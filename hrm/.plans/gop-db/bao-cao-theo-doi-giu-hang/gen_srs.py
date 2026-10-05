# -*- coding: utf-8 -*-
"""Sinh "SRS - Báo cáo theo dõi giữ hàng.docx" theo FORM CHUẨN hiện hành
(bản mẫu `.claude/skills/srs-documenter/assets/SRS_MAU.docx` = "SRS - Phiếu đề nghị thu tiền").

Chạy:  python3 .plans/gop-db/bao-cao-theo-doi-giu-hang/gen_srs.py

Nguồn nội dung: design.md cùng thư mục (bảng "Chốt vướng mắc…" + "Chốt sau nghiệm thu code" A–K
GHI ĐÈ spec), spec docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md,
code nhánh gop_db (hrm-api Modules/Finance/Services/PrepickTracking/*, hrm-client
pages/sale/prepick-tracking/**). Ảnh chụp thật ở `bao-cao-theo-doi-giu-hang_shots/` (1440×900,
dùng chung với test case / HDSD).
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

# Thư viện vẽ UML của skill trỏ cứng font Windows (C:\Windows\Fonts\segoeui.ttf). Máy macOS ->
# trỏ sang font hệ thống CÓ ĐỦ DẤU TIẾNG VIỆT ngay trong generator (monkeypatch), KHÔNG sửa file
# dùng chung trong .claude/skills/.
import srs_uml_render as uml  # noqa: E402

if not os.path.exists(uml.F_REG):
    _MAC = "/System/Library/Fonts/Supplemental"
    for _attr, _name in (("F_REG", "Arial.ttf"), ("F_BOLD", "Arial Bold.ttf"),
                         ("F_ITAL", "Arial Italic.ttf")):
        _path = os.path.join(_MAC, _name)
        if os.path.exists(_path):
            setattr(uml, _attr, _path)

from srs_docx_lib import SrsDoc  # noqa: E402

OUT = os.path.join(HERE, "SRS - Báo cáo theo dõi giữ hàng.docx")
SHOTS = os.path.join(HERE, "bao-cao-theo-doi-giu-hang_shots")
MENU = "Phân hệ Bán hàng => Báo cáo => Hàng giữ => Báo cáo theo dõi giữ hàng"
SCREEN = "Báo cáo theo dõi giữ hàng"

ACT_NV = "Nhân viên kinh doanh đang giữ hàng"
ACT_QL = "Quản lý / Kế toán theo dõi hàng giữ"
TACNHAN = "%s; %s; Người dùng đã đăng nhập" % (ACT_QL, ACT_NV)


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route="/sale/prepick-tracking",
           full_url="https://<host-hrm>/sale/prepick-tracking", img_prefix="ptr_")

# ================================================================= TRANG ĐẦU
d.title_block(SCREEN)
d.h2("Mục lục")
d.toc()

# ================================================================= PHẦN 1
d.h1("Phần 1. Giới thiệu")

d.h2("1 Mục đích")
d.p("Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Báo cáo theo dõi giữ hàng thuộc phân hệ "
    "Bán hàng, nhằm:")
d.bullets([
    "Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho báo cáo theo dõi tồn "
    "hàng ĐANG GIỮ tại thời điểm xem: ai đang giữ, giữ mặt hàng gì, cho khách nào, còn bao lâu "
    "thì hết hạn giữ.",
    "Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.",
    "Làm rõ cơ chế phạm vi dữ liệu: màn hình không chặn quyền truy cập, chỉ một quyền duy nhất "
    "“Xem báo cáo giữ hàng theo tổng công ty” quyết định được xem công ty khác hay không.",
    "Làm rõ các đơn vị đếm dễ hiểu sai: “yêu cầu giữ” (phiếu giữ gốc + mã hàng + nhân viên), đo "
    "bằng số lượng hay số mã hàng theo từng dòng, các nhóm hạn đếm chồng lấn ở dòng gom nhiều mã.",
    "Làm rõ nguồn của các cột lấy từ nghiệp vụ khác: Tồn hiện tại, Số lần gia hạn, Phiếu giữ gốc "
    "và Tổng thanh toán của hợp đồng.",
])

d.h2("2 Thuật ngữ và viết tắt")
d.table(["Thuật ngữ", "Mô tả"], [
    ("Hàng giữ", "Số lượng hàng hoá đang được giữ lại cho một khách hàng, đứng tên một nhân viên "
     "kinh doanh, có ngày bắt đầu giữ và hạn giữ. Hàng giữ không gắn kho và không gắn lô nhập."),
    ("Yêu cầu giữ", "Đơn vị đếm chính của báo cáo = Phiếu giữ gốc + Mã hàng + Nhân viên. Một phiếu "
     "của nhân viên A xin giữ 5 mã hàng được đếm là 5 yêu cầu giữ."),
    ("Phiếu giữ gốc", "Chứng từ đầu tiên sinh ra hàng giữ (Phiếu xuất giữ, Nhập hàng cho khách, "
     "Điều chuyển giữ…), sau khi lần ngược hết các lần gia hạn."),
    ("Hạn giữ hiện tại", "Hạn giữ đang có hiệu lực của phần hàng giữ — có thể đã qua nhiều lần "
     "gia hạn."),
    ("Cảnh báo trước (N ngày)", "Ngưỡng xác định nhóm Sắp hết hạn. Mặc định lấy theo cấu hình hệ "
     "thống (hiện là 7 ngày); người xem đổi được trên thanh lọc mà không ghi đè cấu hình chung."),
    ("Trong hạn / Sắp hết hạn / Hết hạn", "Ba nhóm trạng thái hạn giữ: hạn giữ sau hôm nay + N "
     "ngày / từ hôm nay đến hôm nay + N ngày / trước hôm nay."),
    ("Tiêu chí theo dõi", "Cách bổ dọc bảng: Theo nhân viên (Phòng ban ▸ Nhân viên ▸ Hàng hoá) "
     "hoặc Theo hàng hoá (Hàng hoá ▸ Nhân viên)."),
    ("Nhóm cấp 1", "Dòng cấp ngoài cùng của bảng theo dõi (Phòng ban hoặc Hàng hoá) — đơn vị "
     "phân trang của bảng."),
    ("Hàng giữ của tôi", "Lối tắt lọc báo cáo về đúng hàng giữ đang đứng tên người đăng nhập; chỉ "
     "ở chế độ này mới hiện nút Gia hạn / Huỷ giữ."),
    ("Tổng thanh toán", "Tổng các khoản khách hàng đã thanh toán cho hợp đồng gắn với yêu cầu giữ, "
     "lấy theo phát sinh Có TK 1311 (phải thu khách hàng) của Phiếu thu, Phiếu báo có và Phiếu kế "
     "toán."),
    ("ĐVT", "Đơn vị tính. Báo cáo luôn quy về đơn vị tính cơ bản của hàng hoá."),
], widths=[1.8, 4.2])

# ================================================================= PHẦN 2
d.h1("Phần 2. Phân quyền")

d.h2("1 Danh sách quyền")
d.p("Nhóm quyền thao tác:")
d.table(["Ký hiệu", "Tên quyền", "Tác dụng trên màn hình"], [
    ("—", "(không có)",
     "Màn hình KHÔNG gắn quyền thao tác. Mọi người dùng đã đăng nhập đều mở được báo cáo và dùng "
     "được mọi chức năng (lọc, xem chi tiết, in, xuất Excel). Nút Gia hạn / Huỷ giữ chỉ phụ thuộc "
     "chế độ “Hàng giữ của tôi”, không phụ thuộc quyền."),
], widths=[0.8, 2.0, 3.2])

d.p("Nhóm quyền quyết định phạm vi dữ liệu:")
d.table(["Ký hiệu", "Tên quyền", "Phạm vi dữ liệu"], [
    ("V1", "Xem báo cáo giữ hàng theo tổng công ty",
     "Hiện ô chọn Công ty có thêm mục “Tất cả công ty”; xem được hàng giữ của bất kỳ công ty nào "
     "hoặc của toàn bộ công ty."),
    ("—", "(không có V1)",
     "Ô Công ty bị thay bằng nhãn cố định ghi tên công ty trong hồ sơ nhân sự của người đăng nhập; "
     "xem TOÀN BỘ hàng giữ của công ty đó (không giới hạn phòng ban, không giới hạn “chỉ của tôi”)."),
], widths=[0.8, 2.0, 3.2])
d.p("Ràng buộc bổ sung: không có ngoại lệ cho tài khoản quản trị — mọi người dùng, kể cả Super "
    "admin, chỉ xét theo quyền V1 được gán. Không có V1 thì hệ thống luôn ép phạm vi về công ty "
    "trong hồ sơ, bỏ qua mọi giá trị công ty gửi lên. Hệ quả cần biết khi bàn giao: hàng giữ của "
    "toàn công ty hiển thị cho mọi nhân viên đăng nhập của công ty đó.")

d.h2("2 Ma trận phân quyền")
d.table(["Chức năng", "V1", "Không có quyền nào"], [
    ("FR-01 Xem báo cáo theo dõi giữ hàng", "✅ (công ty tự chọn / tất cả)", "✅ (công ty trong hồ sơ)"),
    ("FR-02 Tìm kiếm và lọc báo cáo", "✅ (có ô chọn Công ty)", "✅ (Công ty là nhãn cố định)"),
    ("FR-03 Hàng giữ của tôi", "✅", "✅"),
    ("FR-04 Cài đặt bộ lọc", "✅", "✅"),
    ("FR-05 Xem chi tiết hàng giữ", "✅", "✅ (trong công ty của mình)"),
    ("FR-06 Xem lịch sử gia hạn", "✅", "✅ (trong công ty của mình)"),
    ("FR-07 Xem chứng từ thanh toán", "✅", "✅ (trong công ty của mình)"),
    ("FR-08 Gia hạn / Huỷ giữ hàng giữ", "✅ (chỉ hàng giữ của mình)", "✅ (chỉ hàng giữ của mình)"),
    ("FR-09 In danh sách", "✅", "✅ (trong công ty của mình)"),
    ("FR-10 Xuất Excel", "✅", "✅ (trong công ty của mình)"),
], widths=[2.6, 1.6, 1.8])

# ================================================================= PHẦN 3
d.h1("Phần 3. Đặc tả chi tiết theo từng chức năng")

d.h2("1 Sơ đồ UML tổng quan")
d.overview_figure2(
    [(ACT_QL, [0, 1]), (ACT_NV, [0, 1])],
    [("FR-01", "Xem báo cáo theo dõi giữ hàng", "view"),
     ("FR-05", "Xem chi tiết hàng giữ", "view")],
    [("FR-02", "Tìm kiếm và lọc báo cáo", "view", "extend", [0], None),
     ("FR-03", "Hàng giữ của tôi", "view", "extend", [0], None),
     ("FR-04", "Cài đặt bộ lọc", "view", "extend", [0], None),
     ("FR-09", "In danh sách", "io", "extend", [0, 1], None),
     ("FR-10", "Xuất Excel", "io", "extend", [0, 1], None),
     ("FR-06", "Xem lịch sử gia hạn", "view", "extend", [1], None),
     ("FR-07", "Xem chứng từ thanh toán", "view", "extend", [1], None),
     ("FR-08", "Gia hạn / Huỷ giữ hàng giữ", "action", "extend", [1],
      "chỉ ở chế độ Hàng giữ của tôi")],
    "Sơ đồ Use Case tổng quan màn Báo cáo theo dõi giữ hàng")

d.h2("2 Đặc tả chi tiết từng chức năng")

# ----------------------------------------------------------------- 2.1
d.h3("2.1 Xem báo cáo theo dõi giữ hàng")
d.p("2.1.1 Giới thiệu")
d.rule_ref("- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các "
           "quy tắc riêng của Báo cáo theo dõi giữ hàng tại phần mô tả chi tiết.", anchor="list")
d.intro_table(
    ten="Xem báo cáo theo dõi giữ hàng",
    mota="Hiển thị tồn hàng đang giữ tại thời điểm xem trong phạm vi công ty của người dùng: dải "
         "tổng hợp hai khối (Phạm vi đang giữ, Tình trạng theo yêu cầu giữ) và bảng theo dõi dạng "
         "cây theo tiêu chí đang chọn, phân trang theo nhóm cấp 1. Mọi con số đều bấm được để mở "
         "danh sách chi tiết.",
    tacnhan=TACNHAN,
    dieukien="Người dùng đã đăng nhập. Màn hình không yêu cầu quyền riêng.",
    chinh="1. Người dùng vào menu Phân hệ Bán hàng → Báo cáo → Hàng giữ → Báo cáo theo dõi giữ hàng.\n"
          "2. Hệ thống xác định phạm vi công ty: có quyền V1 thì theo ô Công ty, không có thì khoá "
          "theo công ty trong hồ sơ nhân sự.\n"
          "3. Hệ thống lấy mặc định tiêu chí Theo nhân viên, cấp bung Đến Nhân viên, ngưỡng cảnh báo "
          "theo cấu hình hệ thống.\n"
          "4. Hệ thống tính dải tổng hợp và dòng TỔNG trên toàn bộ dữ liệu đã lọc, dựng bảng theo "
          "dõi cho trang 1 (25 nhóm cấp 1).\n"
          "5. Màn hình hiển thị kết quả mà không cần bấm Tìm kiếm.",
    phu="• Không có hàng giữ nào trong phạm vi → bảng hiện “Không có hàng giữ nào khớp bộ lọc.”; "
        "dải tổng hợp hiện 0.\n"
        "• Bấm mũi tên ở một dòng cha chưa có dữ liệu cấp con → hệ thống tải riêng cấp con của "
        "dòng đó (vòng quay chờ trên dòng); tải lỗi thì thu dòng lại và báo “Không tải được chi "
        "tiết của \"<tên dòng>\". <lý do>”.\n"
        "• Đổi ô chọn cấp bung → bảng bung/thu theo cấp mới, giữ nguyên trang đang xem.\n"
        "• Bấm Thu gọn ở dải tổng hợp → ẩn hai khối tổng hợp, chỉ còn dòng tóm tắt.\n"
        "• Bảng chưa hiển thị dòng Hàng hoá nào → các cột Đơn vị, Model, Thương hiệu (và Tồn hiện "
        "tại) tự ẩn; bung một nhánh tới Hàng hoá thì các cột hiện lại.",
    dacbiet=None)

d.p("2.1.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("01-bao-cao.png"),
         shot_caption="Màn Báo cáo theo dõi giữ hàng lúc mới truy cập (người dùng không có quyền V1)")
d.figure(shot("01b-bao-cao-thu-bo-loc.png"),
         "Dải tổng hợp và bảng theo dõi Theo nhân viên, cấp bung Đến Nhân viên", width_in=6.2)
d.figure(shot("01d-tat-ca-cap.png"),
         "Bảng bung Tất cả cấp (đến Hàng hoá): hiện thêm cột Đơn vị, Model, Thương hiệu", width_in=6.2)

d.p("2.1.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề trang", "Label", "Hiển thị", "–", "Báo cáo theo dõi giữ hàng",
     "Hiển thị trên thanh tiêu đề."),
    ("Dòng tóm tắt “Tồn hàng giữ tại <ngày>”", "Label", "Hiển thị", "dd/mm/yyyy", "Ngày hiện tại",
     "Kèm số yêu cầu giữ, số nhân viên, số hàng hoá, số khách hàng của toàn bộ dữ liệu đã lọc. "
     "Icon ⓘ giải thích mục đích báo cáo."),
    ("Nút Thu gọn / Mở rộng", "Button", "Enable", "–", "Thu gọn",
     "Ẩn hoặc hiện hai khối tổng hợp."),
    ("Khối Phạm vi đang giữ", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "3 ô đếm phân biệt: Nhân viên đang giữ (người), Hàng hoá bị giữ (mã hàng), Khách hàng "
     "(khách). Góc khối ghi tổng số yêu cầu giữ. Bấm số → mở chi tiết toàn bộ hàng giữ."),
    ("Ô Tổng yêu cầu đang giữ hàng", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Số yêu cầu giữ còn hàng, kèm số mã hàng."),
    ("Ô Yêu cầu sắp hết hạn", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Yêu cầu có ít nhất một phần hàng sắp hết hạn, kèm tỷ lệ % trên tổng yêu cầu. Nền cam."),
    ("Ô Yêu cầu đã hết hạn", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Yêu cầu có ít nhất một phần hàng đã quá hạn, kèm tỷ lệ %. Nền đỏ. Chồng lấn với ô Sắp hết "
     "hạn — không cộng hai ô."),
    ("Ô NV có hàng giữ quá hạn", "Text", "Hiển thị", "≥ 0", "Theo dữ liệu",
     "Số nhân viên có ít nhất một phần hàng quá hạn, kèm “trên N người”. Bấm số → danh sách hàng "
     "quá hạn của các nhân viên đó."),
    ("Icon ⓘ ở tiêu đề khối / ô / cột", "Icon Button", "Enable", "–", "Hiển thị",
     "Rê chuột hiện giải thích cách tính (ngưỡng cảnh báo đang áp, quy tắc chồng lấn…)."),
    ("Bảng theo dõi", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Cột: STT · Nội dung theo dõi · [Đơn vị · Model · Thương hiệu · Tồn hiện tại] · Số lượng giữ "
     "· Trong hạn · Sắp hết hạn · Hết hạn. Cột trong ngoặc chỉ hiện khi bảng có dòng Hàng hoá; Tồn "
     "hiện tại chỉ có ở tiêu chí Theo hàng hoá."),
    ("Nút sắp xếp cột Nội dung theo dõi", "Icon Button", "Enable", "Danh sách 3 trạng thái",
     "Mặc định (⇅)", "A→Z (▲) → Z→A (▼) → về thứ tự mặc định (quá hạn nhiều nhất lên trước). "
     "Đổi thứ tự thì quay về trang 1."),
    ("Ô chọn cấp bung", "Dropdown", "Enable", "Danh sách theo tiêu chí", "Đến Nhân viên",
     "Theo nhân viên: Chỉ Phòng ban / Đến Nhân viên / Tất cả cấp (đến Hàng hoá). Theo hàng hoá: "
     "Chỉ Hàng hoá / Tất cả cấp (đến Nhân viên)."),
    ("Dòng TỔNG", "Label", "Read-only", "≥ 0", "Theo dữ liệu",
     "Luôn tính trên toàn bộ dữ liệu đã lọc, không theo trang. Ghi tên các cấp của tiêu chí."),
    ("Dòng Phòng ban / Nhân viên / Hàng hoá", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Thụt lề theo cấp, có mũi tên bung/thu ở dòng có cấp con. Nhân viên kèm mã nhân viên (tiêu chí "
     "Theo hàng hoá kèm thêm phòng ban). Hàng hoá hiện dạng “Mã hàng - Tên hàng”, tên dài cắt tối "
     "đa 2 dòng, rê chuột xem đủ."),
    ("Ô Số lượng giữ và 3 cột hạn", "Number", "Read-only", "≥ 0", "Theo dữ liệu",
     "Dòng gom đúng 1 mã hàng: số lượng theo ĐVT cơ bản. Dòng gom nhiều mã: số mã hàng kèm chữ "
     "“Mã”. Số khác 0 bấm được để mở chi tiết; số 0 hiện xám, không bấm được. Màu: Trong hạn xanh, "
     "Sắp hết hạn cam, Hết hạn đỏ."),
    ("Cột Tồn hiện tại", "Number", "Read-only", "≥ 0", "Theo dữ liệu",
     "Chỉ ở tiêu chí Theo hàng hoá, dòng Hàng hoá: tồn kho của mặt hàng trong công ty đang lọc "
     "(Tất cả công ty = cộng mọi công ty); dòng khác hiện “—”."),
    ("Phân trang", "Pagination", "Enable", "10 / 25 / 50 / 100", "25 nhóm / trang",
     "Phân trang theo nhóm cấp 1, dòng đếm dạng “Hiển thị a–b / N nhóm”. STT chạy tiếp theo trang."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Không có hàng giữ nào khớp bộ lọc.”"),
    ("Lớp mờ khi đang tải", "Loading", "Hiển thị", "–", "Ẩn",
     "Dữ liệu cũ mờ đi và không bấm được trong lúc tải lại."),
], required=False)

d.p("2.1.4 Danh sách event và xử lý event")
d.event_table([
    ("Mở màn hình", "System",
     "Before:\n– Xác định phạm vi công ty theo quyền V1 ngay trước lần tải đầu (không quyền thì khoá "
     "theo công ty trong hồ sơ).\n"
     "During:\n– Nạp danh mục ô lọc (chỉ giá trị đang có hàng giữ trong phạm vi) và dữ liệu báo cáo "
     "với tiêu chí Theo nhân viên, cấp bung Đến Nhân viên.\n"
     "After:\n– Hiển thị dải tổng hợp, dòng TỔNG và trang 1 của bảng theo dõi."),
    ("Bấm mũi tên ở dòng cha", "Click",
     "Before:\n– Dòng đã có cấp con thì chỉ bung/thu, không tải lại.\n"
     "During:\n– Dòng chưa có cấp con → tải cấp con theo đúng bộ lọc của báo cáo đang hiển thị.\n"
     "After:\n– Hiện cấp con; lỗi thì thu dòng và báo “Không tải được chi tiết của \"<tên>\". <lý do>”."),
    ("Đổi ô chọn cấp bung", "Change",
     "During:\n– Cấp mới sâu hơn dữ liệu đang có → tải lại báo cáo; ngược lại chỉ thu/bung trên màn.\n"
     "After:\n– Giữ nguyên trang đang xem."),
    ("Bấm nút sắp xếp cột Nội dung theo dõi", "Click",
     "During:\n– Chuyển vòng A→Z → Z→A → mặc định; sắp trên toàn bộ dữ liệu rồi mới cắt trang.\n"
     "After:\n– Quay về trang 1."),
    ("Bấm số trang / đổi số dòng mỗi trang", "Click",
     "After:\n– Tải trang mới; dải tổng hợp và dòng TỔNG giữ nguyên. Đổi số dòng → về trang 1."),
    ("Bấm một con số khác 0", "Click",
     "After:\n– Mở popup Chi tiết hàng giữ đúng dòng và đúng chỉ số vừa bấm (FR-05)."),
    ("Bấm Thu gọn / Mở rộng", "Click", "After:\n– Ẩn hoặc hiện hai khối tổng hợp, đổi chữ trên nút."),
])

# ----------------------------------------------------------------- 2.2
d.h3("2.2 Tìm kiếm và lọc báo cáo")
d.p("2.2.1 Giới thiệu")
d.rule_ref("- Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang. Chỉ bổ sung các tiêu chí lọc riêng "
           "của Báo cáo theo dõi giữ hàng.", anchor="search")
d.intro_table(
    ten="Tìm kiếm và lọc báo cáo",
    mota="Thu hẹp phạm vi số liệu của toàn màn (dải tổng hợp, bảng, popup, bản in, Excel) theo tiêu "
         "chí theo dõi, công ty, phòng ban, bộ phận, nhân viên, khách hàng, thương hiệu, model, "
         "trạng thái hạn giữ, ngưỡng cảnh báo, hình thức giữ và từ khoá hàng hoá.",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn Báo cáo theo dõi giữ hàng.",
    chinh="1. Người dùng mở khối Tìm kiếm nâng cao (mặc định đang mở).\n"
          "2. Người dùng chọn giá trị ở các ô lọc dạng chọn → hệ thống tải lại báo cáo ngay.\n"
          "3. Với ô gõ tay (Cảnh báo trước, Tìm hàng hoá) người dùng nhập rồi bấm Enter hoặc Tìm kiếm.\n"
          "4. Hệ thống tính lại dải tổng hợp và bảng theo bộ lọc mới, quay về trang 1.",
    phu="• Chọn Phòng ban → xoá Bộ phận và Nhân viên đang chọn, nạp lại danh sách theo phòng.\n"
        "• Ô Bộ phận: chưa chọn phòng ban → khoá, ghi “Chọn phòng ban trước”; phòng chưa chia bộ "
        "phận → khoá, ghi “Phòng này chưa chia bộ phận”; phòng có bộ phận → liệt kê bộ phận đang "
        "giữ hàng kèm mục “Chưa phân bộ phận” (khi phòng còn nhân viên chưa gán bộ phận).\n"
        "• Chọn Bộ phận → xoá Nhân viên đang chọn, danh sách nhân viên thu theo bộ phận.\n"
        "• Ô Cảnh báo trước nhập ngoài 0–365 hoặc không phải số nguyên → báo đỏ “Nhập số nguyên từ "
        "0 đến 365”, không tải báo cáo cho tới khi sửa.\n"
        "• Bấm Xóa lọc → mọi ô về mặc định NHƯNG giữ Công ty và Tiêu chí theo dõi; tắt chế độ Hàng "
        "giữ của tôi.\n"
        "• Người có quyền V1 đổi Công ty → xoá Phòng ban, Bộ phận, Nhân viên và nạp lại danh mục "
        "theo công ty mới.",
    dacbiet="Mọi ô dạng chọn chỉ liệt kê giá trị THỰC SỰ đang có hàng giữ trong phạm vi được xem "
            "(nhân viên đang giữ, khách hàng đang được giữ, …), không đổ toàn bộ danh mục.")

d.p("2.2.2 Layout màn hình")
d.layout(menu=MENU, shot=shot("02-bo-loc.png"),
         shot_caption="Khối Tìm kiếm nâng cao đang mở với đủ 12 tiêu chí (không có quyền V1: Công ty "
                      "là nhãn cố định, Bộ phận khoá “Chọn phòng ban trước”)")
d.figure(shot("02b-bo-loc-bo-phan.png"),
         "Đã chọn phòng ban có chia bộ phận: ô Bộ phận mở khoá", width_in=6.2)
d.figure(shot("03-co-quyen-cong-ty.png"),
         "Người dùng có quyền V1: ô Công ty chọn được, có mục “Tất cả công ty”", width_in=6.2)
d.figure(shot("01c-theo-hang-hoa.png"),
         "Tiêu chí Theo hàng hoá: cấp 1 là Hàng hoá, có thêm cột Tồn hiện tại", width_in=6.2)

d.p("2.2.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao", "Button", "Enable", "–", "–",
     "Ẩn tìm kiếm nâng cao", "Mở hoặc thu khối ô lọc."),
    ("Tiêu chí theo dõi", "Radio", "Enable", "Danh sách 2 giá trị", "Có", "Theo nhân viên",
     "Theo nhân viên / Theo hàng hoá. Đổi tiêu chí thì cấp bung về mặc định của tiêu chí (Đến Nhân "
     "viên / Chỉ Hàng hoá) và tải lại ngay."),
    ("Công ty (có quyền V1)", "Dropdown", "Enable / Ẩn", "Danh sách công ty + “Tất cả công ty”",
     "Có", "Công ty trong hồ sơ", "Không có nút xoá ×. Chỉ hiện với người có quyền V1."),
    ("Công ty (không có quyền V1)", "Label", "Read-only", "–", "–", "Công ty trong hồ sơ",
     "Nhãn cố định nền xám, rê chuột xem đủ tên. Không đổi được."),
    ("Phòng ban", "Dropdown", "Enable", "Danh sách", "Không", "Trống",
     "Chỉ phòng ban có nhân viên đang giữ hàng."),
    ("Bộ phận", "Dropdown", "Enable / Disable", "Danh sách + “Chưa phân bộ phận”", "Không",
     "Khoá — “Chọn phòng ban trước”", "Ba trạng thái như mô tả ở Dòng sự kiện phụ; không bao giờ "
     "để trống mà không ghi lý do."),
    ("Nhân viên", "Dropdown", "Enable", "Danh sách", "Không", "Trống",
     "Chỉ người đang giữ hàng, khuôn “Tên - Mã phòng - Mã nhân viên”; thu theo phòng ban/bộ phận "
     "đang chọn."),
    ("Khách hàng", "Dropdown", "Enable", "Danh sách", "Không", "Trống",
     "Chỉ khách hàng đang được giữ hàng."),
    ("Thương hiệu", "Dropdown", "Enable", "Danh sách", "Không", "Trống", "Thương hiệu của hàng hoá."),
    ("Model", "Dropdown", "Enable", "Danh sách", "Không", "Trống", "Model của hàng hoá."),
    ("Trạng thái hạn giữ", "Dropdown", "Enable", "Danh sách 3 giá trị", "Không", "Trống (tất cả)",
     "Trong hạn / Sắp hết hạn / Hết hạn."),
    ("Cảnh báo trước (ngày)", "Number", "Enable", "0 – 365, số nguyên", "Không",
     "Trống (gợi ý số ngày cấu hình)", "Trống = theo cấu hình hệ thống. Sai khoảng báo đỏ “Nhập số "
     "nguyên từ 0 đến 365”. Chỉ đổi cách xem, không ghi đè cấu hình chung."),
    ("Hình thức giữ", "Dropdown", "Enable", "Danh sách 2 giá trị", "Không", "Trống (tất cả)",
     "Giữ theo hợp đồng / Không theo hợp đồng."),
    ("Tìm hàng hoá", "Textbox", "Enable", "0–255 ký tự", "Không", "Trống",
     "Tìm theo một phần mã hoặc tên hàng hoá; áp khi Enter hoặc Tìm kiếm."),
    ("Nút Tìm kiếm", "Button", "Enable", "–", "–", "Hiển thị",
     "Áp bộ lọc, quay về trang 1. Không gọi tải khi ô Cảnh báo trước đang báo lỗi."),
    ("Nút Xóa lọc", "Button", "Enable", "–", "–", "Hiển thị",
     "Đưa các ô về mặc định, giữ Công ty và Tiêu chí theo dõi, tắt Hàng giữ của tôi."),
    ("Icon ⓘ cạnh nhãn ô lọc", "Icon Button", "Enable", "–", "–", "Hiển thị",
     "Giải thích ý nghĩa ô (Tiêu chí, Công ty, Bộ phận, Nhân viên, Trạng thái, Cảnh báo trước, Hình "
     "thức giữ)."),
])

d.p("2.2.4 Danh sách event và xử lý event")
d.event_table([
    ("Đổi một ô lọc dạng chọn", "Change",
     "Before:\n– Người không có quyền V1 đổi Công ty → bỏ qua (phạm vi bị khoá).\n"
     "During:\n– Xoá các ô con theo chuỗi Công ty ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên; nạp lại danh "
     "mục khi đổi Công ty hoặc Phòng ban.\n– Đang bật Hàng giữ của tôi mà đổi Tiêu chí / Công ty / "
     "Phòng ban / Bộ phận / Nhân viên → tắt chế độ đó nhưng giữ lựa chọn vừa đổi.\n"
     "After:\n– Tải lại báo cáo, quay về trang 1."),
    ("Nhập ô Cảnh báo trước / Tìm hàng hoá", "Keypress",
     "During:\n– Chỉ ghi nhận giá trị, chưa tải.\n– Cảnh báo trước sai khoảng → báo đỏ “Nhập số "
     "nguyên từ 0 đến 365”.\n"
     "After:\n– Enter hoặc bấm Tìm kiếm → tải lại báo cáo nếu không còn lỗi."),
    ("Bấm Tìm kiếm", "Click",
     "Before:\n– Ô Cảnh báo trước đang báo lỗi → không thực hiện.\n"
     "After:\n– Tải lại báo cáo theo bộ lọc, quay về trang 1; bộ lọc này áp cho popup, bản in và "
     "Excel."),
    ("Bấm Xóa lọc", "Click",
     "After:\n– Đưa các ô về mặc định, GIỮ Công ty và Tiêu chí; tắt Hàng giữ của tôi; nạp lại danh "
     "mục và báo cáo, quay về trang 1."),
])

# ----------------------------------------------------------------- 2.3
d.h3("2.3 Hàng giữ của tôi")
d.p("2.3.1 Biểu đồ Usecase")
d.uc_figure("FR-03", "Hàng giữ của tôi", "view",
            [("include", "Ép bộ lọc về hàng giữ đứng tên người đăng nhập"),
             ("extend", "Khôi phục bộ lọc trước khi bật"),
             ("extend", "Hiện nút Gia hạn / Huỷ giữ trong popup chi tiết")],
            actor=ACT_NV, caption="Biểu đồ Use Case — FR-03 Hàng giữ của tôi")
d.p("2.3.2 Giới thiệu")
d.rule_ref("- Bộ lọc và Thông báo. Chỉ bổ sung cách lối tắt “Hàng giữ của tôi” ép và khôi phục bộ "
           "lọc của Báo cáo theo dõi giữ hàng.", anchor="search")
d.intro_table(
    ten="Hàng giữ của tôi",
    mota="Lối tắt bật/tắt ở đầu thanh lọc: một lần bấm lọc báo cáo về đúng hàng giữ đang đứng tên "
         "người đăng nhập, bung sẵn tới cấp Hàng hoá, và mở các nút Gia hạn / Huỷ giữ trong popup "
         "chi tiết.",
    tacnhan="%s; Người dùng đã đăng nhập" % ACT_NV,
    dieukien="Đang ở màn Báo cáo theo dõi giữ hàng.",
    chinh="1. Người dùng bấm nút Hàng giữ của tôi.\n"
          "2. Hệ thống chụp lại 6 giá trị đang chọn (Tiêu chí, Công ty, Phòng ban, Bộ phận, Nhân "
          "viên, Cấp bung).\n"
          "3. Hệ thống ép: Tiêu chí Theo nhân viên · công ty của tôi · phòng ban của tôi · bộ phận "
          "của tôi · nhân viên = tôi · cấp bung Tất cả cấp (đến Hàng hoá).\n"
          "4. Nút chuyển nền xanh đặc; hệ thống tải lại báo cáo, quay về trang 1.",
    phu="• Bấm lại chính nút đó → tắt chế độ và khôi phục ĐÚNG 6 giá trị đã chụp (không về mặc định).\n"
        "• Đổi tay Tiêu chí / Công ty / Phòng ban / Bộ phận / Nhân viên khi đang bật → tắt chế độ, "
        "giữ lựa chọn vừa đổi, không khôi phục.\n"
        "• Bấm Xóa lọc → tắt chế độ.\n"
        "• Người không có quyền V1 → không đụng tới Công ty (vốn đã khoá theo hồ sơ).\n"
        "• Người chưa được gán bộ phận → Bộ phận để “tất cả”, không ép “Chưa phân bộ phận”.\n"
        "• Người đăng nhập không giữ hàng nào → bảng rỗng, ô Nhân viên vẫn ghi tên mình.",
    dacbiet=None)
d.p("2.3.3 Layout màn hình")
d.layout(menu=MENU + " => Hàng giữ của tôi", shot=shot("04-hang-giu-cua-toi.png"),
         shot_caption="Chế độ Hàng giữ của tôi đang bật: bảng bung tới Hàng hoá của chính người đăng nhập")
d.p("2.3.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Hàng giữ của tôi (tắt)", "Button", "Enable", "–", "Hiển thị",
     "Nút viền trắng, icon người; rê chuột hiện giải thích."),
    ("Nút Hàng giữ của tôi (bật)", "Button", "Enable", "–", "Ẩn",
     "Nút nền xanh đặc — báo hiệu báo cáo đang ở chế độ lọc riêng."),
    ("Các ô bị ép giá trị", "Dropdown", "Enable", "–", "Theo hồ sơ người đăng nhập",
     "Tiêu chí, Công ty (chỉ khi có quyền V1), Phòng ban, Bộ phận, Nhân viên — vẫn đổi tay được."),
    ("Ô chọn cấp bung", "Dropdown", "Enable", "–", "Tất cả cấp (đến Hàng hoá)",
     "Đã bó về 1 người nên bung thẳng tới Hàng hoá."),
    ("Bảng theo dõi", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Chỉ hàng giữ đứng tên người đăng nhập; bấm số mở popup chi tiết có nút Gia hạn / Huỷ giữ."),
], required=False)
d.p("2.3.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Hàng giữ của tôi (đang tắt)", "Click",
     "Before:\n– Chưa xác định được người đăng nhập → không làm gì.\n"
     "During:\n– Chụp 6 giá trị, ép bộ lọc như Dòng sự kiện chính.\n"
     "After:\n– Nạp lại danh mục ô lọc và báo cáo, quay về trang 1."),
    ("Bấm Hàng giữ của tôi (đang bật)", "Click",
     "After:\n– Khôi phục 6 giá trị đã chụp, tắt chế độ, tải lại báo cáo về trang 1."),
    ("Đổi tay ô bị ép khi đang bật", "Change",
     "After:\n– Tắt chế độ, giữ giá trị vừa chọn, tải lại báo cáo."),
])

# ----------------------------------------------------------------- 2.4
d.h3("2.4 Cài đặt bộ lọc")
d.p("2.4.1 Biểu đồ Usecase")
d.uc_figure("FR-04", "Cài đặt bộ lọc", "view",
            [("include", "Lưu cấu hình theo từng người dùng"),
             ("extend", "Khôi phục cấu hình mặc định")],
            actor="Người dùng đã đăng nhập", caption="Biểu đồ Use Case — FR-04 Cài đặt bộ lọc")
d.p("2.4.2 Giới thiệu")
d.rule_ref("- Cấu hình bộ lọc. Chỉ bổ sung danh sách tiêu chí lọc riêng của Báo cáo theo dõi giữ "
           "hàng.", anchor="excel")
d.intro_table(
    ten="Cài đặt bộ lọc",
    mota="Cho mỗi người dùng tự chọn các ô lọc hiển thị trong khối Tìm kiếm nâng cao và thứ tự của "
         "chúng. Cấu hình lưu riêng cho màn hình này.",
    tacnhan="Người dùng đã đăng nhập",
    dieukien="Đang ở màn Báo cáo theo dõi giữ hàng.",
    chinh="1. Người dùng bấm nút Cài đặt bộ lọc.\n"
          "2. Hệ thống mở cửa sổ với 12 tiêu chí, đánh số và tích theo cấu hình đang lưu.\n"
          "3. Người dùng tích/bỏ tích, kéo biểu tượng ⠿ để đổi thứ tự.\n"
          "4. Người dùng bấm Lưu.\n"
          "5. Hệ thống lưu cấu hình, đóng cửa sổ, báo “Cập nhật thành công” và vẽ lại khối lọc.",
    phu="• Bấm Khôi phục mặc định → về đúng thứ tự gốc, tích đủ 12 tiêu chí; phải bấm Lưu mới ghi.\n"
        "• Bấm Đóng hoặc × → bỏ mọi thay đổi chưa lưu.\n"
        "• Lưu lỗi → báo “Thao tác thất bại”, giữ cửa sổ.\n"
        "• Ẩn một ô đang có giá trị → giá trị của ô đó được xoá khỏi bộ lọc.",
    dacbiet=None)
d.p("2.4.3 Layout màn hình")
d.layout(menu=MENU + " => Cài đặt bộ lọc", modal="Cài đặt bộ lọc",
         shot=shot("05-cai-dat-bo-loc.png"), shot_caption="Cửa sổ Cài đặt bộ lọc với đủ 12 tiêu chí")
d.p("2.4.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề cửa sổ", "Label", "Hiển thị", "–", "–", "Cài đặt bộ lọc", "Kèm icon bánh răng."),
    ("Dòng hướng dẫn", "Label", "Hiển thị", "–", "–", "Hiển thị",
     "“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn "
     "hình.”"),
    ("Ô tích từng tiêu chí", "Checkbox", "Enable", "Danh sách 12 tiêu chí", "Không",
     "Theo cấu hình đã lưu", "Tiêu chí theo dõi, Công ty, Phòng ban, Bộ phận, Nhân viên, Khách "
     "hàng, Thương hiệu, Model, Trạng thái hạn giữ, Cảnh báo trước (ngày), Hình thức giữ, Tìm hàng "
     "hoá."),
    ("Tay kéo ⠿", "Icon Button", "Enable", "–", "–", "Hiển thị", "Kéo để đổi thứ tự."),
    ("Nút Lưu", "Button", "Enable", "–", "–", "Hiển thị", "Khoá trong lúc đang lưu."),
    ("Nút Khôi phục mặc định", "Button", "Enable", "–", "–", "Hiển thị", "Chưa ghi, phải bấm Lưu."),
    ("Nút Đóng / ×", "Button", "Enable", "–", "–", "Hiển thị", "Đóng, bỏ thay đổi chưa lưu."),
])
d.p("2.4.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Cài đặt bộ lọc", "Click", "After:\n– Mở cửa sổ, nạp cấu hình đang lưu."),
    ("Bấm Lưu", "Click",
     "During:\n– Ghi cấu hình (tiêu chí hiển thị + thứ tự) cho người dùng hiện tại.\n"
     "After:\n– Thành công: đóng cửa sổ, báo “Cập nhật thành công”, vẽ lại khối lọc.\n"
     "– Lỗi: báo “Thao tác thất bại”."),
    ("Bấm Khôi phục mặc định", "Click", "After:\n– Đưa danh sách về thứ tự gốc, tích đủ 12 tiêu chí."),
])

# ----------------------------------------------------------------- 2.5
d.h3("2.5 Xem chi tiết hàng giữ")
d.p("2.5.1 Giới thiệu")
d.rule_ref("- Màn Xem chi tiết, Bộ lọc, Sắp xếp dữ liệu bảng và Phân trang. Chỉ bổ sung bộ cột và "
           "quy tắc riêng của popup chi tiết hàng giữ.", anchor="detail")
d.intro_table(
    ten="Xem chi tiết hàng giữ",
    mota="Popup liệt kê từng phần hàng giữ tạo nên con số vừa bấm (ở dải tổng hợp, dòng TỔNG hoặc "
         "một dòng của bảng), có ô lọc, sắp xếp 7 cột, phân trang và ghim 3 cột đầu khi cuộn ngang.",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn báo cáo và bấm vào một con số khác 0.",
    chinh="1. Người dùng bấm một con số.\n"
          "2. Hệ thống mở popup với tiêu đề “Đang xem <chỉ số> theo <cấp>: <tên dòng>” (bấm từ toàn "
          "báo cáo: “— toàn bộ báo cáo”), dòng phụ ghi đường dẫn các cấp cha.\n"
          "3. Hệ thống tải trang 1 (20 dòng), sắp mặc định theo hạn giữ tăng dần (quá hạn lâu nhất "
          "lên đầu).\n"
          "4. Dòng đếm hiện “N mã hàng · M yêu cầu giữ · ĐVT: …” trên toàn bộ kết quả lọc.",
    phu="• Popup mở từ một Nhân viên → ẩn cột Nhân viên giữ và Phòng ban; mở từ một Phòng ban → ẩn "
        "cột Phòng ban (thông tin đã nằm ở tiêu đề).\n"
        "• Popup mở từ một trạng thái cụ thể (Trong hạn / Sắp hết hạn / Hết hạn / NV có hàng giữ "
        "quá hạn) → ẩn cột và ô lọc Trạng thái.\n"
        "• Mở từ một Hàng hoá → ẩn ô lọc Hàng hoá, cột Mã hàng - Tên hàng vẫn hiện.\n"
        "• Mở từ Yêu cầu sắp/đã hết hạn → liệt kê TOÀN BỘ phần hàng của các yêu cầu trúng nhóm "
        "(nhiều hơn số phần hàng thuần ở trạng thái đó).\n"
        "• Không có dòng nào → “Không có hàng giữ nào khớp bộ lọc.”\n"
        "• Bấm phóng to → popup phủ kín màn hình; 3 cột ghim đo lại vị trí.",
    dacbiet=None)
d.p("2.5.2 Layout màn hình")
d.layout(menu=MENU + " => Bấm vào con số => Chi tiết hàng giữ", modal="Chi tiết hàng giữ",
         shot=shot("06-popup-chi-tiet.png"),
         shot_caption="Popup Chi tiết hàng giữ mở từ dòng TỔNG (toàn bộ báo cáo)")
d.figure(shot("06b-popup-ghim-cot.png"),
         "Cuộn ngang popup: 3 cột STT, Mã hàng - Tên hàng, ĐVT được ghim", width_in=6.2)
d.p("2.5.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề popup + dòng đường dẫn", "Label", "Hiển thị", "–", "–", "Theo con số được bấm",
     "Hàng hoá dạng “Mã hàng - Tên hàng”, nhân viên dạng “Tên - Phòng ban”."),
    ("Ô tìm nhanh", "Textbox", "Enable", "0–255 ký tự", "Không", "Trống",
     "Tìm theo mã/tên hàng hoá, khách hàng, nhân viên, mã phiếu giữ gốc; tự áp sau khi ngừng gõ "
     "hoặc Enter."),
    ("Ô lọc Nhân viên / Khách hàng / Hàng hoá / Trạng thái", "Dropdown", "Enable / Ẩn",
     "Danh sách", "Không", "Tất cả", "Chỉ liệt kê giá trị có trong tập của con số vừa bấm. Ẩn theo "
     "quy tắc ở Dòng sự kiện phụ."),
    ("Nút Xoá lọc (popup)", "Button", "Enable / Ẩn", "–", "–", "Ẩn",
     "Hiện khi có ít nhất 1 ô lọc của popup đang có giá trị."),
    ("Dòng đếm", "Label", "Read-only", "–", "–", "Theo dữ liệu",
     "“N mã hàng · M yêu cầu giữ · ĐVT: …” (quá 3 đơn vị thì ghi “K đơn vị tính”)."),
    ("Bảng chi tiết", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu",
     "15 cột: STT · Mã hàng - Tên hàng · ĐVT · SL đang giữ · Ngày bắt đầu giữ · Hạn giữ hiện tại · "
     "Số lần gia hạn · Thương hiệu / Model · Khách hàng · Số hợp đồng · Tổng thanh toán · Nhân viên "
     "giữ · Phòng ban · Trạng thái · Phiếu giữ gốc. Ghim 3 cột đầu khi cuộn ngang."),
    ("Tiêu đề cột sắp xếp được", "Icon Button", "Enable", "7 cột", "–", "Hạn giữ tăng dần",
     "Mã hàng - Tên hàng, SL đang giữ, Khách hàng, Nhân viên giữ, Phòng ban, Ngày bắt đầu giữ, Hạn "
     "giữ hiện tại; chu kỳ tăng → giảm → mặc định."),
    ("Ô Hạn giữ hiện tại", "Text", "Read-only", "dd/mm/yyyy", "–", "Theo dữ liệu",
     "Kèm “còn N ngày” / “hết hạn hôm nay” / “quá hạn N ngày”; tô xanh / cam / đỏ theo trạng thái."),
    ("Ô Số lần gia hạn", "Number", "Read-only", "≥ 0", "–", "Theo dữ liệu",
     "Số khác 0 bấm được → popup Lịch sử gia hạn (FR-06)."),
    ("Ô Số hợp đồng", "Text", "Read-only", "–", "–", "Theo dữ liệu",
     "Không gắn hợp đồng ghi “Không theo hợp đồng”."),
    ("Ô Tổng thanh toán", "Number", "Read-only", "≥ 0", "–", "Theo dữ liệu",
     "Không theo hợp đồng hiện “—”; số khác 0 bấm được → popup chứng từ (FR-07)."),
    ("Ô Trạng thái", "Badge", "Read-only", "Danh sách 3 giá trị", "–", "Theo dữ liệu",
     "Trong hạn (xanh) / Sắp hết hạn (cam) / Hết hạn (đỏ)."),
    ("Ô Phiếu giữ gốc", "Text", "Read-only", "–", "–", "Theo dữ liệu",
     "Mã chứng từ gốc; có đường dẫn thì bấm mở ở tab mới, rê chuột hiện loại chứng từ. Không xác "
     "định được hiện “—”."),
    ("Phân trang", "Pagination", "Enable", "20 / 50 / 100", "–", "20 dòng / trang",
     "“Hiển thị a–b / N dòng”, STT chạy tiếp theo trang."),
    ("Nút phóng to / ×", "Icon Button", "Enable", "–", "–", "Hiển thị", "Phủ kín màn hình / đóng."),
    ("Nút In danh sách · Xuất Excel · Đóng", "Button", "Enable", "–", "–", "Hiển thị",
     "In và Excel theo bộ lọc + thứ tự đang áp của popup (FR-09, FR-10); Đóng ở cuối."),
])
d.p("2.5.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm một con số trên màn báo cáo", "Click",
     "Before:\n– Chụp lại bộ lọc của báo cáo đang hiển thị và cờ Hàng giữ của tôi.\n"
     "During:\n– Xác định tập hàng giữ theo dòng + chỉ số được bấm, trong phạm vi công ty.\n"
     "After:\n– Mở popup với ô lọc trống, thứ tự mặc định, trang 1."),
    ("Đổi ô lọc / gõ ô tìm nhanh", "Change",
     "After:\n– Tải lại danh sách, quay về trang 1; dòng đếm tính trên toàn bộ kết quả lọc."),
    ("Bấm tiêu đề cột sắp xếp được", "Click",
     "After:\n– Chuyển vòng tăng → giảm → mặc định, sắp trên toàn bộ rồi cắt trang, về trang 1."),
    ("Cuộn ngang bảng", "System",
     "After:\n– 3 cột STT, Mã hàng - Tên hàng, ĐVT đứng yên, các cột còn lại trượt."),
    ("Bấm Đóng / ×", "Click", "After:\n– Đóng popup, màn báo cáo giữ nguyên bộ lọc và trang."),
])

# ----------------------------------------------------------------- 2.6
d.h3("2.6 Xem lịch sử gia hạn")
d.p("2.6.1 Giới thiệu")
d.rule_ref("- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung cách lần ngược chuỗi gia hạn của "
           "một phần hàng giữ.", anchor="history")
d.intro_table(
    ten="Xem lịch sử gia hạn",
    mota="Popup liệt kê từng lần gia hạn của đúng phần hàng giữ đang xem, xếp từ cũ đến mới; lần "
         "cuối (hạn đang có hiệu lực) được tô nền.",
    tacnhan=TACNHAN,
    dieukien="Đang mở popup Chi tiết hàng giữ; ô Số lần gia hạn của dòng khác 0.",
    chinh="1. Người dùng bấm số ở cột Số lần gia hạn.\n"
          "2. Hệ thống kiểm tra dòng nằm trong phạm vi công ty được xem.\n"
          "3. Hệ thống lần ngược chuỗi gia hạn của dòng đó và trả các lần gia hạn cũ → mới.\n"
          "4. Popup hiển thị dòng mô tả và bảng lịch sử.",
    phu="• Dòng không thuộc phạm vi xem → hệ thống báo “Không tìm thấy hàng giữ”.\n"
        "• Chưa có lần gia hạn nào → “Chưa có lần gia hạn nào.”\n"
        "• Bấm mã phiếu gia hạn (khi có đường dẫn) → mở phiếu ở tab mới.",
    dacbiet=None)
d.p("2.6.2 Layout màn hình")
d.layout(menu=MENU + " => Chi tiết hàng giữ => Số lần gia hạn", modal="Lịch sử gia hạn giữ hàng",
         shot=shot("07-lich-su-gia-han.png"), shot_caption="Popup Lịch sử gia hạn giữ hàng (2 lần gia hạn)")
d.p("2.6.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề popup", "Label", "Hiển thị", "–", "Lịch sử gia hạn giữ hàng", "Kèm icon lịch sử."),
    ("Dòng mô tả", "Label", "Read-only", "–", "Theo dữ liệu",
     "“Mã hàng - Tên hàng · ĐVT · Khách hàng · Nhân viên giữ · Đã gia hạn N lần · Phiếu giữ gốc”."),
    ("Bảng lịch sử", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Cột: Lần · Ngày duyệt · Phiếu gia hạn · Hạn cũ → Hạn mới · SL gia hạn · Người đề nghị · "
     "Người duyệt. Không phân trang."),
    ("Ô Hạn cũ → Hạn mới", "Text", "Read-only", "dd/mm/yyyy", "Theo dữ liệu",
     "Hạn cũ gạch ngang, hạn mới in đậm."),
    ("Ô SL gia hạn", "Number", "Read-only", "≥ 0", "Theo dữ liệu", "Quy về ĐVT cơ bản."),
    ("Dòng lần cuối", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Tô nền — hạn đang có hiệu lực."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Chưa có lần gia hạn nào.”"),
    ("Nút Đóng / ×", "Button", "Enable", "–", "Hiển thị", "Đóng, quay lại popup chi tiết."),
], required=False)
d.p("2.6.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm số ở cột Số lần gia hạn", "Click",
     "Before:\n– Dòng không thuộc phạm vi công ty được xem → báo “Không tìm thấy hàng giữ”, dừng.\n"
     "After:\n– Mở popup, hiển thị các lần gia hạn cũ → mới, tô nền lần cuối."),
    ("Bấm Đóng / ×", "Click", "After:\n– Đóng popup lịch sử, popup chi tiết vẫn mở."),
])

# ----------------------------------------------------------------- 2.7
d.h3("2.7 Xem chứng từ thanh toán")
d.p("2.7.1 Giới thiệu")
d.rule_ref("- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung nguồn số liệu thanh toán của hợp đồng gắn "
           "với hàng giữ.", anchor="detail")
d.intro_table(
    ten="Xem chứng từ thanh toán",
    mota="Popup liệt kê các chứng từ tạo nên con số Tổng thanh toán của hợp đồng gắn với yêu cầu "
         "giữ: Phiếu thu, Phiếu báo có, Phiếu kế toán có phát sinh Có TK 1311 theo hợp đồng đó.",
    tacnhan=TACNHAN,
    dieukien="Đang mở popup Chi tiết hàng giữ; dòng giữ theo hợp đồng và Tổng thanh toán khác 0.",
    chinh="1. Người dùng bấm số ở cột Tổng thanh toán.\n"
          "2. Hệ thống kiểm tra hợp đồng có gắn với ít nhất một phần hàng giữ trong phạm vi xem.\n"
          "3. Hệ thống gom các chứng từ thanh toán của hợp đồng, mỗi chứng từ một dòng, xếp mới → cũ.\n"
          "4. Popup hiển thị dòng mô tả và bảng chứng từ.",
    phu="• Hợp đồng không thuộc phạm vi xem → hệ thống báo “Không tìm thấy hợp đồng”.\n"
        "• Không có chứng từ → “Chưa có chứng từ thanh toán nào.”\n"
        "• Giá trị hợp đồng bằng 0 → tỷ lệ đã thanh toán hiện “—”.",
    dacbiet="Popup KHÔNG hiển thị “Còn phải thu”: đây chỉ là tổng các khoản đã thanh toán, chưa phải "
            "công nợ (công nợ còn phụ thuộc giảm giá, thuế, bù trừ…).")
d.p("2.7.2 Layout màn hình")
d.layout(menu=MENU + " => Chi tiết hàng giữ => Tổng thanh toán", modal="Thanh toán của hợp đồng",
         shot=shot("08-chung-tu-thanh-toan.png"),
         shot_caption="Popup Thanh toán của hợp đồng (Phiếu thu và Phiếu kế toán)")
d.p("2.7.3 Mô tả chi tiết giao diện")
d.ui_table([
    ("Tiêu đề popup", "Label", "Hiển thị", "–", "Thanh toán của hợp đồng <số hợp đồng>", "–"),
    ("Dòng mô tả", "Label", "Read-only", "–", "Theo dữ liệu",
     "Khách hàng · Giá trị hợp đồng (sau thuế) · Đã thanh toán (tỷ lệ %) · Số chứng từ."),
    ("Bảng chứng từ", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Cột: STT · Số chứng từ · Loại chứng từ · Ngày hạch toán · Số tiền. Xếp mới → cũ, không phân "
     "trang."),
    ("Ô Loại chứng từ", "Text", "Read-only", "Danh sách 3 giá trị", "Theo dữ liệu",
     "Phiếu thu / Phiếu báo có / Phiếu kế toán."),
    ("Ô Số tiền", "Number", "Read-only", "≥ 0", "Theo dữ liệu",
     "Tổng phát sinh Có TK 1311 của chứng từ theo hợp đồng, quy đổi VND."),
    ("Trạng thái rỗng", "Label", "Hiển thị", "–", "Ẩn", "“Chưa có chứng từ thanh toán nào.”"),
    ("Nút Đóng / ×", "Button", "Enable", "–", "Hiển thị", "Đóng, quay lại popup chi tiết."),
], required=False)
d.p("2.7.4 Danh sách event và xử lý event")
d.event_table([
    ("Bấm số ở cột Tổng thanh toán", "Click",
     "Before:\n– Hợp đồng không gắn với hàng giữ nào trong phạm vi công ty được xem → báo “Không tìm "
     "thấy hợp đồng”, dừng.\n"
     "After:\n– Mở popup, hiển thị chứng từ mới → cũ và tổng đã thanh toán."),
    ("Bấm Đóng / ×", "Click", "After:\n– Đóng popup, popup chi tiết vẫn mở."),
])

# ----------------------------------------------------------------- 2.8
d.h3("2.8 Gia hạn / Huỷ giữ hàng giữ")
d.p("2.8.1 Biểu đồ Usecase")
d.uc_figure("FR-08", "Gia hạn / Huỷ giữ hàng giữ", "action",
            [("include", "Mở màn lập yêu cầu gia hạn hàng giữ"),
             ("include", "Mở màn lập yêu cầu hủy hàng giữ"),
             ("extend", "Báo “còn N ngày mới tới hạn” khi chưa tới ngưỡng")],
            actor=ACT_NV, caption="Biểu đồ Use Case — FR-08 Gia hạn / Huỷ giữ hàng giữ")
d.p("2.8.2 Giới thiệu")
d.rule_ref("- Thông báo và UI/UX. Chỉ bổ sung điều kiện hiển thị 2 nút điều hướng và cách màn đích "
           "nhận dòng được bấm.", anchor="notice")
d.intro_table(
    ten="Gia hạn / Huỷ giữ hàng giữ",
    mota="Hai nút điều hướng nằm trong ô Hạn giữ hiện tại của popup chi tiết, giúp người đang giữ "
         "hàng lập ngay Yêu cầu gia hạn hàng giữ hoặc Yêu cầu hủy hàng giữ cho đúng dòng vừa xem.",
    tacnhan="%s; Người dùng đã đăng nhập" % ACT_NV,
    dieukien="Chế độ Hàng giữ của tôi đang bật khi mở popup Chi tiết hàng giữ.",
    chinh="1. Người dùng bật Hàng giữ của tôi và bấm một con số để mở popup chi tiết.\n"
          "2. Mỗi dòng hiện 2 nút Gia hạn và Huỷ giữ dưới ngày hạn giữ.\n"
          "3. Bấm Gia hạn → hệ thống chuyển sang màn Thêm yêu cầu gia hạn hàng giữ kèm dòng được "
          "bấm; dòng đã tới ngưỡng gia hạn được tích sẵn “Cần gia hạn” và cuộn tới.\n"
          "4. Bấm Huỷ giữ → hệ thống chuyển sang màn Thêm yêu cầu hủy hàng giữ, điền sẵn khách hàng "
          "và dòng hàng tương ứng.",
    phu="• Ngoài chế độ Hàng giữ của tôi → không có nút nào (danh sách là hàng của người khác).\n"
        "• Dòng chưa tới ngưỡng gia hạn → màn gia hạn hiện ghi chú vàng “Hàng này còn N ngày mới "
        "tới hạn, chưa lập được yêu cầu gia hạn (chỉ lập được khi còn ≤ <ngưỡng> ngày).”\n"
        "• Dòng không còn hàng hoặc không thuộc người đăng nhập → màn gia hạn báo “Không tìm thấy "
        "hàng giữ cần gia hạn hoặc hàng này không thuộc về bạn.”\n"
        "• Màn hủy giữ luôn nhắc “Hủy giữ trừ theo hạn giữ sớm nhất của cùng hàng hoá – khách hàng, "
        "kiểm lại số lượng trước khi gửi.”",
    dacbiet="Hai nút chỉ ĐIỀU HƯỚNG, chưa ghi dữ liệu nên không hỏi xác nhận; hộp xác nhận nằm ở "
            "nút Lưu / Gửi duyệt của màn đích. Nút không xuất hiện trên bản in và file Excel.")
d.p("2.8.3 Layout màn hình")
d.layout(menu=MENU + " => Hàng giữ của tôi => Chi tiết hàng giữ => Gia hạn / Huỷ giữ",
         modal="Chi tiết hàng giữ", shot=shot("09-popup-nut-gia-han-huy.png"),
         shot_caption="Popup chi tiết ở chế độ Hàng giữ của tôi: nút Gia hạn / Huỷ giữ trong ô Hạn giữ hiện tại")
d.figure(shot("10-man-gia-han-thong-bao.png"),
         "Bấm Gia hạn ở dòng còn 60 ngày: màn gia hạn báo chưa lập được yêu cầu", width_in=6.2)
d.figure(shot("11-man-huy-giu.png"),
         "Bấm Huỷ giữ: màn Thêm yêu cầu hủy hàng giữ điền sẵn khách hàng và dòng hàng", width_in=6.2)
d.p("2.8.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Gia hạn", "Button", "Enable / Ẩn", "–", "Ẩn ngoài chế độ Hàng giữ của tôi",
     "Nút viền xanh, icon lịch + chữ; hiện ở mọi dòng kể cả dòng Trong hạn."),
    ("Nút Huỷ giữ", "Button", "Enable / Ẩn", "–", "Ẩn ngoài chế độ Hàng giữ của tôi",
     "Nút viền đỏ, icon dấu × + chữ."),
    ("Ghi chú trên màn gia hạn", "Toast / Alert", "Hiển thị", "–", "Ẩn",
     "Ghi chú vàng (thông tin, không phải lỗi) khi dòng chưa tới ngưỡng hoặc không tìm thấy."),
    ("Ghi chú trên màn hủy giữ", "Label", "Hiển thị", "–", "Hiển thị khi mở từ báo cáo",
     "Chữ xám nhắc hủy theo hạn sớm nhất của cùng hàng hoá – khách hàng."),
], required=False)
d.p("2.8.5 Danh sách event và xử lý event")
d.event_table([
    ("Mở popup chi tiết", "System",
     "Before:\n– Chỉ khi báo cáo đang hiển thị được tải ở chế độ Hàng giữ của tôi mới hiện 2 nút.\n"
     "After:\n– Mỗi dòng có 2 nút trong ô Hạn giữ hiện tại."),
    ("Bấm Gia hạn", "Click",
     "After:\n– Chuyển sang màn Thêm yêu cầu gia hạn hàng giữ kèm dòng được bấm.\n"
     "– Dòng trong danh sách được gia hạn → tích sẵn Cần gia hạn, cuộn tới dòng.\n"
     "– Dòng chưa tới ngưỡng → ghi chú “Hàng này còn N ngày mới tới hạn, chưa lập được yêu cầu "
     "gia hạn (chỉ lập được khi còn ≤ <ngưỡng> ngày).”\n"
     "– Không tìm thấy → “Không tìm thấy hàng giữ cần gia hạn hoặc hàng này không thuộc về bạn.”"),
    ("Bấm Huỷ giữ", "Click",
     "After:\n– Chuyển sang màn Thêm yêu cầu hủy hàng giữ, điền sẵn khách hàng và dòng hàng, hiện "
     "ghi chú về cách trừ theo hạn sớm nhất."),
])

# ----------------------------------------------------------------- 2.9
d.h3("2.9 In danh sách")
d.p("2.9.1 Biểu đồ Usecase")
d.uc_figure("FR-09", "In danh sách", "io",
            [("include", "Chọn chế độ in: bảng theo dõi / danh sách chi tiết"),
             ("include", "Lấy toàn bộ dữ liệu theo bộ lọc đang hiển thị"),
             ("extend", "In danh sách từ popup chi tiết")],
            actor=ACT_QL, caption="Biểu đồ Use Case — FR-09 In danh sách")
d.p("2.9.2 Giới thiệu")
d.rule_ref("- Thông báo và UI/UX. Chỉ bổ sung bố cục và dữ liệu riêng của bản in Báo cáo theo dõi "
           "giữ hàng.", anchor="notice")
d.intro_table(
    ten="In danh sách",
    mota="In báo cáo khổ A4 ngang qua popup xem trước, ở 2 chế độ: In bảng theo dõi (đủ mọi cấp) "
         "hoặc In danh sách chi tiết (từng phần hàng giữ một dòng). Từ popup chi tiết in đúng danh "
         "sách của popup đó.",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn báo cáo (nút ở thanh tiêu đề) hoặc popup Chi tiết hàng giữ (nút ở chân "
             "popup).",
    chinh="1. Người dùng bấm In danh sách ở thanh tiêu đề.\n"
          "2. Hệ thống mở cửa sổ chọn chế độ, mặc định In bảng theo dõi.\n"
          "3. Người dùng chọn chế độ và bấm In.\n"
          "4. Hệ thống dựng bản in theo bộ lọc của báo cáo ĐANG HIỂN THỊ, lấy toàn bộ dữ liệu (không "
          "theo trang, không theo cấp đang bung).\n"
          "5. Popup xem trước hiện bản in; người dùng bấm In để mở hộp thoại in của trình duyệt.",
    phu="• Bấm In danh sách ở chân popup chi tiết → in thẳng danh sách chi tiết theo bộ lọc và thứ "
        "tự đang áp của popup (không qua cửa sổ chọn chế độ).\n"
        "• Danh sách vượt 2.000 dòng → không hiện bản xem trước và nút In, chỉ hiện “Danh sách có N "
        "dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời "
        "gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”\n"
        "• Không có dữ liệu → “Không có dữ liệu để in”.\n"
        "• Bấm Hủy hoặc × ở cửa sổ chọn chế độ → đóng, không in.",
    dacbiet="Bản in có dòng “Bộ lọc đang áp dụng” (chỉ ghi ô có giá trị) để phân biệt 2 bản in của 2 "
            "bộ lọc. Bảng theo dõi: cấp 3 (Hàng hoá) không lùi đầu dòng, cấp 2 (Nhân viên) in đậm và "
            "lùi 1 nấc; dòng gom nhiều mã ghi “N Mã”. Tên hàng in đủ, không cắt.")
d.p("2.9.3 Layout màn hình")
d.layout(menu=MENU + " => In danh sách", modal="In danh sách", shot=shot("12-in-chon-che-do.png"),
         shot_caption="Cửa sổ chọn chế độ In danh sách")
d.figure(shot("13-ban-in-bang-theo-doi.png"), "Bản xem trước In bảng theo dõi", width_in=6.2)
d.figure(shot("14-ban-in-chi-tiet.png"), "Bản xem trước In danh sách chi tiết", width_in=6.2)
d.p("2.9.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút In danh sách (thanh tiêu đề)", "Button", "Enable", "–", "–", "Hiển thị",
     "Mở cửa sổ chọn chế độ."),
    ("Dòng ghi chú cửa sổ", "Label", "Hiển thị", "–", "–", "Hiển thị",
     "“Bản in A4 ngang, bám đúng bộ lọc báo cáo đang hiển thị.”"),
    ("Chế độ in", "Radio", "Enable", "Danh sách 2 giá trị", "Có", "In bảng theo dõi",
     "In bảng theo dõi / In danh sách chi tiết, mỗi lựa chọn có dòng mô tả. Mở lại cửa sổ thì về "
     "mặc định."),
    ("Nút In · Hủy", "Button", "Enable", "–", "–", "Hiển thị", "In dựng bản xem trước; Hủy đóng cửa sổ."),
    ("Popup xem trước", "Modal", "Hiển thị", "–", "–", "Ẩn",
     "Tiêu đề “Xem trước báo cáo theo dõi giữ hàng” / “Xem trước danh sách chi tiết hàng giữ” / "
     "“Xem trước danh sách hàng giữ” (từ popup); nút In mở hộp thoại in."),
    ("Bản in bảng theo dõi", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu",
     "Tiêu đề BÁO CÁO THEO DÕI GIỮ HÀNG, Ngày in, Bộ lọc đang áp dụng; cột STT · Nội dung theo dõi "
     "· Đơn vị · Model · Thương hiệu · [Tồn hiện tại] · Số lượng giữ · Trong hạn · Sắp hết hạn · "
     "Hết hạn; dòng TỔNG đầu bảng."),
    ("Bản in danh sách chi tiết", "Table/Grid", "Read-only", "–", "–", "Theo dữ liệu",
     "Tiêu đề CHI TIẾT HÀNG GIỮ; đủ 15 cột như popup, ô hạn giữ kèm “còn/quá hạn N ngày”, không có "
     "nút Gia hạn / Huỷ giữ."),
    ("Thông báo vượt trần in", "Toast / Alert", "Hiển thị", "> 2.000 dòng", "–", "Ẩn",
     "Câu nhắc thu hẹp bộ lọc hoặc dùng Xuất Excel."),
])
d.p("2.9.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm In danh sách (thanh tiêu đề)", "Click", "After:\n– Mở cửa sổ chọn chế độ, mặc định In bảng theo dõi."),
    ("Bấm In trong cửa sổ chọn chế độ", "Click",
     "Before:\n– Lấy bộ lọc của báo cáo đang hiển thị (không lấy ô lọc đã sửa mà chưa bấm Tìm kiếm).\n"
     "During:\n– Dựng toàn bộ dữ liệu: bảng theo dõi đủ mọi cấp, hoặc danh sách chi tiết của toàn "
     "báo cáo.\n– Vượt 2.000 dòng → chỉ trả thông báo vượt trần.\n"
     "After:\n– Đóng cửa sổ chọn, mở popup xem trước."),
    ("Bấm In danh sách ở chân popup chi tiết", "Click",
     "During:\n– Lấy bộ lọc của báo cáo + bộ lọc và thứ tự đang áp trong popup.\n"
     "After:\n– Mở popup xem trước danh sách chi tiết."),
    ("Bấm In trên popup xem trước", "Click", "After:\n– Mở hộp thoại in của trình duyệt, khổ A4 ngang."),
])

# ----------------------------------------------------------------- 2.10
d.h3("2.10 Xuất Excel")
d.p("2.10.1 Biểu đồ Usecase")
d.uc_figure("FR-10", "Xuất Excel", "io",
            [("include", "Lấy toàn bộ dữ liệu theo bộ lọc đang hiển thị"),
             ("extend", "Xuất danh sách chi tiết từ popup")],
            actor=ACT_QL, caption="Biểu đồ Use Case — FR-10 Xuất Excel")
d.p("2.10.2 Giới thiệu")
d.rule_ref("- Quy tắc Excel. Chỉ bổ sung bộ cột và cách trình bày cây của file Excel Báo cáo theo dõi "
           "giữ hàng.", anchor="excel")
d.intro_table(
    ten="Xuất Excel",
    mota="Tải file Excel của bảng theo dõi (đủ mọi cấp, nút ở thanh tiêu đề) hoặc của danh sách chi "
         "tiết (nút ở chân popup chi tiết), lấy toàn bộ dữ liệu theo bộ lọc.",
    tacnhan=TACNHAN,
    dieukien="Đang ở màn báo cáo hoặc popup Chi tiết hàng giữ.",
    chinh="1. Người dùng bấm Xuất Excel ở thanh tiêu đề.\n"
          "2. Hệ thống dựng file bảng theo dõi theo bộ lọc của báo cáo đang hiển thị, đủ mọi cấp, "
          "không theo trang.\n"
          "3. Trình duyệt tải file “bao-cao-theo-doi-giu-hang.xlsx”.",
    phu="• Bấm Xuất Excel ở chân popup chi tiết → tải “chi-tiet-hang-giu.xlsx”, 15 cột như popup, "
        "theo bộ lọc + thứ tự đang áp của popup.\n"
        "• Lỗi khi tạo đường tải → báo “Lỗi khi xuất Excel”.",
    dacbiet="File Excel không giới hạn số dòng (khác bản in). Ô số là số thật có phân cách hàng "
            "nghìn; dòng gom nhiều mã ghi “Mã” ở cột Đơn vị. Thụt lề cây giống bản in: cấp 2 in đậm "
            "lùi 1 nấc, cấp 3 không lùi. Đầu file có tiêu đề và dòng tóm tắt bộ lọc.")
d.p("2.10.3 Layout màn hình")
d.layout(menu=MENU + " => Xuất Excel", shot=shot("15-xuat-excel.png"),
         shot_caption="Nút Xuất Excel trên thanh tiêu đề của báo cáo")
d.p("2.10.4 Mô tả chi tiết giao diện")
d.ui_table([
    ("Nút Xuất Excel (thanh tiêu đề)", "Button", "Enable", "–", "Hiển thị",
     "Nút xanh lá, icon Excel. Xuất bảng theo dõi."),
    ("Nút Xuất Excel (chân popup chi tiết)", "Button", "Enable", "–", "Hiển thị",
     "Nút xanh lá. Xuất danh sách chi tiết."),
    ("File bảng theo dõi", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "Tiêu đề BÁO CÁO THEO DÕI GIỮ HÀNG, dòng bộ lọc; cột STT · Nội dung theo dõi · Đơn vị · Model "
     "· Thương hiệu · [Tồn hiện tại] · Số lượng giữ · Trong hạn · Sắp hết hạn · Hết hạn; dòng TỔNG."),
    ("File danh sách chi tiết", "Table/Grid", "Read-only", "–", "Theo dữ liệu",
     "15 cột như popup, không có nút Gia hạn / Huỷ giữ."),
], required=False)
d.p("2.10.5 Danh sách event và xử lý event")
d.event_table([
    ("Bấm Xuất Excel (thanh tiêu đề)", "Click",
     "Before:\n– Lấy bộ lọc của báo cáo đang hiển thị, bỏ trang và cấp bung.\n"
     "During:\n– Dựng bảng theo dõi đủ mọi cấp trên toàn bộ dữ liệu.\n"
     "After:\n– Trình duyệt tải file bao-cao-theo-doi-giu-hang.xlsx; lỗi → “Lỗi khi xuất Excel”."),
    ("Bấm Xuất Excel (popup chi tiết)", "Click",
     "Before:\n– Lấy bộ lọc báo cáo + bộ lọc và thứ tự của popup.\n"
     "After:\n– Tải file chi-tiet-hang-giu.xlsx với toàn bộ dòng (không theo trang)."),
])

# ================================================================= PHẦN 4
d.h1("Phần 4. Quy tắc nghiệp vụ")
d.rule_ref(". Phần này chỉ ghi các quy tắc đặc thù của Báo cáo theo dõi giữ hàng; không lặp lại các "
           "quy tắc đã có trong SRS quy tắc chung.",
           anchor="list", head="Quy tắc áp dụng",
           lead="Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ")

d.rule_table([
    ("BR-01", "Báo cáo là ảnh chụp tồn giữ tại thời điểm xem", [
        "– Báo cáo chỉ gồm phần hàng giữ còn số lượng lớn hơn 0 tại lúc xem; không có bộ lọc kỳ.",
        "– Phần hàng đã xuất hết, đã hủy hết hoặc đã chuyển hết sang hạn mới không còn trong báo cáo.",
        "– Số lượng giữ luôn tính theo đơn vị tính cơ bản của hàng hoá; báo cáo không có chế độ đổi "
        "đơn vị.",
    ], "Toàn màn hình"),
    ("BR-02", "Phạm vi công ty theo một quyền duy nhất", [
        "– Màn hình không chặn truy cập: mọi người dùng đã đăng nhập đều mở được.",
        "– Có quyền “Xem báo cáo giữ hàng theo tổng công ty”: chọn một công ty bất kỳ hoặc “Tất cả "
        "công ty”.",
        "– Không có quyền: hệ thống luôn ép về công ty trong hồ sơ nhân sự, bỏ qua giá trị công ty "
        "gửi lên; xem toàn bộ hàng giữ của công ty đó, không giới hạn phòng ban.",
        "– Không có ngoại lệ cho tài khoản quản trị (kể cả Super admin) — chỉ xét quyền được gán.",
        "– Nút Xóa lọc và lối tắt Hàng giữ của tôi không làm thay đổi phạm vi công ty của người "
        "không có quyền.",
        "– Popup lịch sử gia hạn và chứng từ thanh toán chỉ mở được cho dòng / hợp đồng thuộc phạm vi "
        "công ty được xem.",
    ], ["Xem báo cáo", "Tìm kiếm và lọc", "Xem chi tiết", "In", "Xuất Excel"]),
    ("BR-03", "Ba nhóm trạng thái hạn giữ", [
        "– Trong hạn: hạn giữ sau ngày hôm nay + N ngày. Sắp hết hạn: hạn giữ từ hôm nay đến hôm "
        "nay + N ngày. Hết hạn: hạn giữ trước hôm nay. Ba nhóm chia hết tổng của một phần hàng.",
        "– N lấy từ ô Cảnh báo trước (số nguyên 0–365); để trống thì theo cấu hình hệ thống (hiện "
        "là 7 ngày). Đổi N chỉ đổi cách xem báo cáo, không ghi đè cấu hình chung.",
        "– Màu thống nhất toàn màn: Trong hạn xanh, Sắp hết hạn cam, Hết hạn đỏ.",
    ], ["Xem báo cáo", "Tìm kiếm và lọc", "Xem chi tiết"]),
    ("BR-04", "Đơn vị đếm “yêu cầu giữ”", [
        "– 1 yêu cầu giữ = Phiếu giữ gốc + Mã hàng + Nhân viên. Một phiếu xin giữ 5 mã hàng được "
        "đếm là 5 yêu cầu giữ.",
        "– Yêu cầu sắp hết hạn / đã hết hạn = yêu cầu có ít nhất một phần hàng ở nhóm đó; hai nhóm "
        "chồng lấn nhau, không cộng lại thành tổng.",
        "– NV có hàng giữ quá hạn đếm số người khác nhau có ít nhất một phần hàng quá hạn.",
        "– Bấm số của Yêu cầu sắp/đã hết hạn mở toàn bộ phần hàng của các yêu cầu trúng nhóm.",
    ], ["Xem báo cáo", "Xem chi tiết"]),
    ("BR-05", "Lần ngược phiếu giữ gốc qua chuỗi gia hạn", [
        "– Mỗi lần gia hạn tạo phần hàng giữ mới với hạn mới; chứng từ trực tiếp của phần hàng đó là "
        "phiếu gia hạn, không phải chứng từ gốc.",
        "– Cột Phiếu giữ gốc và khoá đếm yêu cầu giữ luôn lấy chứng từ ĐẦU CHUỖI (Phiếu xuất giữ, "
        "Nhập hàng cho khách, Điều chuyển giữ…), không lấy mã phiếu gia hạn.",
        "– Số lần gia hạn = độ dài chuỗi gia hạn của chính phần hàng đó; chỉ hiện trong popup chi "
        "tiết, không cộng dồn lên bảng theo dõi.",
    ], ["Xem chi tiết", "Xem lịch sử gia hạn"]),
    ("BR-06", "Đo bằng số lượng hay số mã — quyết định theo từng dòng", [
        "– Dòng gom đúng 1 mã hàng: hiện SỐ LƯỢNG theo đơn vị tính cơ bản (3 cột hạn chia hết cột "
        "Số lượng giữ).",
        "– Dòng gom nhiều mã hàng: hiện SỐ MÃ HÀNG kèm chữ “Mã”; 3 cột hạn đếm chồng lấn (một mã "
        "vừa có hàng trong hạn vừa có hàng quá hạn) nên tổng 3 cột có thể lớn hơn cột Số lượng giữ.",
        "– Áp như nhau cho màn hình, bản in và Excel. Khi bộ lọc chỉ còn 1 mã hàng thì cả dòng TỔNG "
        "cũng hiện số lượng.",
    ], ["Xem báo cáo", "In", "Xuất Excel"]),
    ("BR-07", "Cấu trúc cây và phân trang", [
        "– Theo nhân viên: Phòng ban ▸ Nhân viên ▸ Hàng hoá. Theo hàng hoá: Hàng hoá ▸ Nhân viên.",
        "– Bảng phân trang theo NHÓM CẤP 1 (mặc định 25, chọn 10/25/50/100), mỗi trang kèm toàn bộ "
        "cấp con; STT chạy tiếp theo trang.",
        "– Dải tổng hợp và dòng TỔNG luôn tính trên toàn bộ dữ liệu đã lọc, không theo trang.",
        "– Về trang 1 khi đổi bộ lọc, tiêu chí, ngưỡng cảnh báo, Xóa lọc, bật/tắt Hàng giữ của tôi "
        "hoặc đổi sắp xếp; đổi cấp bung thì giữ trang.",
        "– Bộ phận chỉ là ô lọc, không phải một cấp của cây.",
    ], ["Xem báo cáo"]),
    ("BR-08", "Thứ tự mặc định và sắp xếp", [
        "– Bảng theo dõi: nhóm có nhiều phần hàng quá hạn lên trước, rồi nhiều phần hàng hơn, rồi "
        "theo tên. Sắp theo tên: A→Z → Z→A → về mặc định.",
        "– Popup chi tiết: hạn giữ tăng dần (quá hạn lâu nhất lên đầu); 7 cột sắp được, chu kỳ tăng "
        "→ giảm → mặc định.",
        "– Lịch sử gia hạn xếp cũ → mới; chứng từ thanh toán xếp mới → cũ.",
        "– Sắp trên toàn bộ dữ liệu rồi mới cắt trang.",
    ], ["Xem báo cáo", "Xem chi tiết", "Xem lịch sử gia hạn", "Xem chứng từ thanh toán"]),
    ("BR-09", "Tồn hiện tại chỉ ở tiêu chí Hàng hoá", [
        "– Tồn hiện tại = tổng số lượng còn trong các kho của công ty đang lọc; “Tất cả công ty” "
        "thì cộng tồn mọi công ty.",
        "– Chỉ hiện ở dòng Hàng hoá khi xem Theo hàng hoá; không có ở tiêu chí Theo nhân viên và "
        "không có trong popup chi tiết (tồn là số của cả công ty, không so được với hàng giữ của "
        "từng nhân viên).",
    ], ["Xem báo cáo", "In", "Xuất Excel"]),
    ("BR-10", "Nguồn của Tổng thanh toán", [
        "– Chỉ có ở hàng giữ theo hợp đồng; hàng giữ không theo hợp đồng ghi “Không theo hợp đồng”, "
        "cột tiền “—”.",
        "– Tổng thanh toán = tổng phát sinh Có TK 1311 (phải thu khách hàng) gắn với hợp đồng, của "
        "3 loại chứng từ: Phiếu thu, Phiếu báo có, Phiếu kế toán; quy đổi VND.",
        "– Không trừ phát sinh Nợ 1311, không cộng số dư đầu kỳ hay tài khoản khác.",
        "– Không hiển thị “Còn phải thu” — đây không phải công nợ.",
    ], ["Xem chi tiết", "Xem chứng từ thanh toán"]),
    ("BR-11", "Danh mục ô lọc và ô Bộ phận", [
        "– Mọi ô lọc dạng chọn chỉ liệt kê giá trị đang có hàng giữ trong phạm vi được xem.",
        "– Bộ phận có 3 trạng thái: khoá “Chọn phòng ban trước”; khoá “Phòng này chưa chia bộ "
        "phận”; mở với các bộ phận đang giữ hàng + mục “Chưa phân bộ phận” khi phòng còn nhân viên "
        "chưa gán bộ phận.",
        "– Đổi Công ty xoá Phòng ban, Bộ phận, Nhân viên; đổi Phòng ban xoá Bộ phận, Nhân viên; đổi "
        "Bộ phận xoá Nhân viên.",
        "– Xóa lọc giữ nguyên Công ty và Tiêu chí theo dõi.",
    ], ["Tìm kiếm và lọc"]),
    ("BR-12", "Lối tắt Hàng giữ của tôi", [
        "– Bật: ép Tiêu chí Theo nhân viên, công ty / phòng ban / bộ phận / nhân viên của người đăng "
        "nhập, cấp bung tới Hàng hoá; không đụng công ty khi không có quyền; chưa gán bộ phận thì để "
        "tất cả.",
        "– Tắt bằng chính nút: khôi phục đúng bộ lọc trước khi bật. Đổi tay ô bị ép hoặc Xóa lọc: "
        "tắt chế độ, giữ lựa chọn mới.",
    ], ["Hàng giữ của tôi"]),
    ("BR-13", "Nút Gia hạn / Huỷ giữ", [
        "– Chỉ hiện khi popup mở từ báo cáo đang ở chế độ Hàng giữ của tôi; là nút điều hướng, không "
        "hỏi xác nhận.",
        "– Màn gia hạn chỉ cho lập yêu cầu với phần hàng còn ≤ số ngày cảnh báo theo cấu hình; dòng "
        "còn xa hạn hiện ghi chú “Hàng này còn N ngày mới tới hạn, chưa lập được yêu cầu gia hạn…”.",
        "– Hủy giữ trừ theo hạn giữ sớm nhất của cùng hàng hoá – khách hàng, không đảm bảo trừ đúng "
        "dòng vừa bấm; màn hủy giữ nhắc người dùng kiểm lại số lượng.",
    ], ["Gia hạn / Huỷ giữ hàng giữ"]),
    ("BR-14", "In và Excel lấy toàn bộ dữ liệu", [
        "– In / Xuất Excel lấy theo bộ lọc của báo cáo ĐANG HIỂN THỊ, toàn bộ trang, đủ mọi cấp bất "
        "kể cấp đang bung; từ popup thì theo bộ lọc + thứ tự của popup.",
        "– Bản in A4 ngang, có dòng Bộ lọc đang áp dụng; vượt 2.000 dòng thì không in, nhắc thu hẹp "
        "bộ lọc hoặc dùng Excel. Excel không giới hạn dòng.",
        "– Bảng theo dõi trên bản in và Excel: cấp 3 không lùi đầu dòng, cấp 2 in đậm lùi 1 nấc; tên "
        "hàng in đủ.",
        "– Bản in lấy letterhead theo công ty đang lọc; xem “Tất cả công ty” thì không in letterhead.",
    ], ["In danh sách", "Xuất Excel"]),
])



def split_hyperlink_rels(doc):
    """Mỗi đoạn "Quy tắc chung" một liên kết RIÊNG (như bản mẫu sau khi Word lưu lại).

    python-docx gộp các hyperlink cùng URL vào MỘT quan hệ, nên đoạn dùng lại cùng anchor (vd 2 lần
    anchor 'excel') chỉ ra 1 liên kết và srs_selfcheck đếm thiếu. Bản mẫu `SRS_MAU.docx` có 13
    quan hệ riêng cho 13 đoạn (Word tách khi cập nhật mục lục) — máy Mac không chạy được bước Word
    đó, nên tách tay ở đây: cùng URL, chỉ khác mã quan hệ. KHÔNG đổi URL / anchor.
    """
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
# Máy Mac không có PowerShell/COM để Word cập nhật mục lục -> bỏ bước đó (mở file trong Word rồi
# Update Field để có số trang).
d.save(update_fields=False)
