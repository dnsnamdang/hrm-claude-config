# -*- coding: utf-8 -*-
"""Sinh 2 tai lieu MO TA NGHIEP VU (skill business-flow-documenter):
  - "Mô tả nghiệp vụ - Kế hoạch bán hàng của nhân viên.docx"              (#11884)
  - "Mô tả nghiệp vụ - Kế hoạch phát triển thị trường của nhân viên.docx" (#11885)

Hai man dung chung khung (luong duyet, cay thang -> tinh, chi tieu, lay du lieu cheo) -> 1 ham build(P),
phan khac nhau nam trong KINDS. Doi chieu code worktree develop (20/11/2026).
Chay: python3 gen_mo_ta_nghiep_vu.py
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = "20/11/2026"

# ───────────────────────── Tham số riêng từng màn ─────────────────────────
KINDS = {
    "sale": {
        "issue": "#11884",
        "ten": "Kế hoạch bán hàng của nhân viên",
        "ngan": "kế hoạch bán hàng",
        "prefix": "KHBHNV",
        "path": "/finance/sale-plan-employees",
        "kia": "Kế hoạch phát triển thị trường của nhân viên",
        "kia_ngan": "KH phát triển thị trường",
        "nut_lay": "Lấy dữ liệu từ KH phát triển thị trường",
        "q_xem": "Xem danh sách kế hoạch bán hàng",
        "q_duyet": "Trưởng phòng duyệt kế hoạch bán hàng nhân viên",
        "menu": "Bán hàng → Kế hoạch → Kế hoạch bán hàng → Của nhân viên",
        "menu_duyet": "Bán hàng → Phê Duyệt → Kế hoạch & chỉ tiêu → KH bán hàng chờ duyệt",
        "erp_menu": "Kinh doanh → Kế hoạch → Kế hoạch bán hàng → Kế hoạch bán hàng của nhân viên",
        "erp_menu_duyet": "Chờ duyệt → Kế hoạch - Chỉ tiêu → Kế hoạch bán hàng → Kế hoạch bán hàng của nhân viên chờ duyệt",
        "muc_dich": (
            "Mỗi nhân viên kinh doanh tự lập kế hoạch bán hàng cho cả năm của mình: từng tháng, ở từng Tỉnh/TP "
            "sẽ làm việc với bao nhiêu khách, ký bao nhiêu hợp đồng hàng hóa và hợp đồng dịch vụ, doanh số "
            "tiêu chuẩn của các hợp đồng đó, doanh số tiêu chuẩn quyết toán và doanh số xuất hàng dự kiến. "
            "Kế hoạch được đặt cạnh chỉ tiêu kinh doanh mà công ty đã giao cho chính nhân viên đó để nhân viên "
            "và trưởng phòng thấy ngay kế hoạch đang hụt hay vượt chỉ tiêu ở tỉnh nào. Trưởng phòng duyệt rồi "
            "gửi lên Ban giám đốc."
        ),
        "vi_tri_pheu": (
            "Kế hoạch bán hàng là CUỐI phễu (hợp đồng). Đầu phễu là Kế hoạch phát triển thị trường của nhân viên "
            "(báo giá). Hai kế hoạch nối với nhau bằng hệ số chuyển đổi: cứ bao nhiêu báo giá thì ra một hợp đồng."
        ),
        "cot": [
            ["DS tiêu chuẩn quyết toán", "Doanh số tiêu chuẩn dự kiến quyết toán được trong tháng ở tỉnh đó.", "Không bắt buộc"],
            ["Doanh số xuất hàng", "Doanh số hàng dự kiến xuất trong tháng ở tỉnh đó (cột mới, bản cũ không có).", "Không bắt buộc"],
            ["SL khách", "Số khách hàng dự kiến làm việc. Nhập tay, thay cho việc liệt kê từng khách như bản cũ.",
             "Bắt buộc khi dòng đã chọn Tỉnh/TP"],
            ["Hợp đồng hàng hóa — SL HĐ / DS tiêu chuẩn", "Số hợp đồng hàng hóa và doanh số tiêu chuẩn của chúng.",
             "Đi theo cặp: nhập ô này thì phải nhập ô kia"],
            ["Hợp đồng dịch vụ — SL HĐ / DS tiêu chuẩn", "Số hợp đồng dịch vụ và doanh số tiêu chuẩn của chúng.",
             "Đi theo cặp: nhập ô này thì phải nhập ô kia"],
            ["Tổng cộng — SL HĐ / DS tiêu chuẩn", "Hàng hóa + dịch vụ. Hệ thống tự cộng, không nhập.", "Không nhập"],
        ],
        "dk_gui": "tổng DS tiêu chuẩn (cột Tổng cộng) của cả phiếu phải lớn hơn 0",
        "loi_gui": "Phiếu chưa có DS tiêu chuẩn hợp đồng — không gửi được",
        "cot_ds": "SL khách · SL HĐ · DS tiêu chuẩn · DSTC quyết toán (ẩn sẵn) · DS xuất hàng (ẩn sẵn)",
        "chi_tieu_hien": (
            "Ngay dưới dòng TỔNG và dưới mỗi Tỉnh/TP có thêm dòng “Chỉ tiêu giao”: số khách chỉ tiêu (hàng hóa + "
            "dịch vụ) đặt dưới cột SL khách; doanh số chỉ tiêu hàng hóa đặt dưới DS tiêu chuẩn của Hợp đồng hàng "
            "hóa; doanh số chỉ tiêu dịch vụ đặt dưới DS tiêu chuẩn của Hợp đồng dịch vụ; tổng doanh số chỉ tiêu "
            "đặt dưới DS tiêu chuẩn của Tổng cộng."
        ),
        "huong": "chia",
        "quy_doi": [
            ["SL HĐ hàng hóa / dịch vụ", "SL báo giá ÷ hệ số, làm tròn; tối thiểu 1 nếu có báo giá, bằng 0 nếu không có báo giá"],
            ["DS tiêu chuẩn hàng hóa / dịch vụ", "Giá trị báo giá ÷ hệ số, làm tròn tới hàng nghìn; tối thiểu 1,000 nếu có giá trị"],
            ["SL khách", "SL HĐ hàng hóa + SL HĐ dịch vụ vừa tính"],
            ["DS tiêu chuẩn quyết toán", "DS tiêu chuẩn hàng hóa + DS tiêu chuẩn dịch vụ vừa tính"],
            ["Doanh số xuất hàng", "Bằng DS tiêu chuẩn quyết toán"],
        ],
        "vi_du": "Hệ số 3: 9 báo giá hàng hóa trị giá 300,000,000 sẽ thành 3 hợp đồng hàng hóa, DS tiêu chuẩn 100,000,000.",
        "khac_rieng": [
            ["So với chỉ tiêu được giao", "Chặn không cho lưu khi kế hoạch chưa đạt chỉ tiêu.",
             "Chỉ HIỂN THỊ so sánh ở tab Theo thị trường, không chặn lưu / gửi.",
             "Theo bản chốt của khách: nhân viên được lập kế hoạch thấp hơn chỉ tiêu, trưởng phòng nhìn so sánh để duyệt."],
            ["Giá trị hợp đồng", "Có cột giá trị hợp đồng bên cạnh doanh số tiêu chuẩn.",
             "Bỏ, chỉ còn SL HĐ và DS tiêu chuẩn; thêm cột Doanh số xuất hàng.",
             "Theo bản chốt của khách."],
        ],
    },
    "market": {
        "issue": "#11885",
        "ten": "Kế hoạch phát triển thị trường của nhân viên",
        "ngan": "kế hoạch phát triển thị trường",
        "prefix": "KHTTNV",
        "path": "/finance/market-plan-employees",
        "kia": "Kế hoạch bán hàng của nhân viên",
        "kia_ngan": "KH bán hàng",
        "nut_lay": "Lấy dữ liệu từ KH bán hàng",
        "q_xem": "Xem danh sách lập kế hoạch thị trường",
        "q_duyet": "Trưởng phòng duyệt kế hoạch thị trường nhân viên",
        "menu": "Bán hàng → Kế hoạch → Kế hoạch phát triển thị trường → Theo nhân viên",
        "menu_duyet": "Bán hàng → Phê Duyệt → Kế hoạch & chỉ tiêu → KH PTTT chờ duyệt",
        "erp_menu": "Kinh doanh → Kế hoạch → Kế hoạch phát triển thị trường → Kế hoạch phát triển thị trường theo nhân viên",
        "erp_menu_duyet": ("Chờ duyệt → Kế hoạch - Chỉ tiêu → Kế hoạch phát triển thị trường → Kế hoạch phát triển "
                           "thị trường theo nhân viên chờ duyệt"),
        "muc_dich": (
            "Mỗi nhân viên kinh doanh tự lập kế hoạch phát triển thị trường cho cả năm của mình: từng tháng, ở "
            "từng Tỉnh/TP sẽ tiếp cận bao nhiêu khách, gửi bao nhiêu báo giá hàng hóa và báo giá dịch vụ, tổng "
            "giá trị các báo giá đó. Kế hoạch được đặt cạnh chỉ tiêu kinh doanh mà công ty đã giao cho chính nhân "
            "viên đó để thấy lượng báo giá có đủ nuôi chỉ tiêu hay không. Trưởng phòng duyệt rồi gửi lên Ban "
            "giám đốc."
        ),
        "vi_tri_pheu": (
            "Kế hoạch phát triển thị trường là ĐẦU phễu (báo giá). Cuối phễu là Kế hoạch bán hàng của nhân viên "
            "(hợp đồng). Hai kế hoạch nối với nhau bằng hệ số chuyển đổi: cứ bao nhiêu báo giá thì ra một hợp đồng."
        ),
        "cot": [
            ["SL khách", "Số khách hàng dự kiến tiếp cận. Nhập tay, thay cho việc liệt kê từng khách như bản cũ.",
             "Bắt buộc khi dòng đã chọn Tỉnh/TP"],
            ["Báo giá hàng hóa — SL / Giá trị", "Số báo giá hàng hóa và tổng giá trị của chúng.",
             "Đi theo cặp: nhập ô này thì phải nhập ô kia"],
            ["Báo giá dịch vụ — SL / Giá trị", "Số báo giá dịch vụ và tổng giá trị của chúng.",
             "Đi theo cặp: nhập ô này thì phải nhập ô kia"],
            ["Tổng cộng — SL / Giá trị", "Hàng hóa + dịch vụ. Hệ thống tự cộng, không nhập.", "Không nhập"],
        ],
        "dk_gui": "tổng Giá trị báo giá (cột Tổng cộng) của cả phiếu phải lớn hơn 0",
        "loi_gui": "Phiếu chưa có giá trị báo giá — không gửi được",
        "cot_ds": "SL khách · SL báo giá · Giá trị báo giá",
        "chi_tieu_hien": (
            "Bên phải bảng có thêm 4 cột “Chỉ tiêu giao — Hàng hóa” và “Chỉ tiêu giao — Dịch vụ”, mỗi nhóm gồm "
            "SL khách và Doanh số, hiện ở dòng TỔNG và ở từng Tỉnh/TP."
        ),
        "huong": "nhân",
        "quy_doi": [
            ["SL báo giá hàng hóa / dịch vụ", "SL HĐ hàng hóa / dịch vụ × hệ số"],
            ["Giá trị báo giá hàng hóa / dịch vụ", "DS tiêu chuẩn hàng hóa / dịch vụ × hệ số"],
            ["SL khách", "SL khách của kế hoạch bán hàng × hệ số"],
        ],
        "vi_du": "Hệ số 3: 2 hợp đồng hàng hóa có DS tiêu chuẩn 100,000,000 sẽ thành 6 báo giá hàng hóa, giá trị 300,000,000.",
        "khac_rieng": [
            ["Chỉ tiêu được giao", "Không đọc chỉ tiêu; chọn Tỉnh/TP bất kỳ.",
             "Chỉ chọn Tỉnh/TP có trong chỉ tiêu được giao; tab Theo thị trường hiện 4 cột chỉ tiêu để so sánh (không chặn lưu).",
             "Theo bản chốt của khách: kế hoạch thị trường phải bám đúng địa bàn được giao."],
        ],
    },
}


def build(kind):
    P = KINDS[kind]
    out = os.path.join(HERE, "Mô tả nghiệp vụ - %s.docx" % P["ten"])
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    path_tables = []  # bảng chương 9 — cột Đường dẫn được phép ghi route màn

    def h(text, level):
        doc.add_paragraph(text, style="Heading %d" % level)

    def para(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            r = p.add_run(bold_prefix)
            r.bold = True
        p.add_run(text)
        return p

    def bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style="List Bullet")
        if bold_prefix:
            r = p.add_run(bold_prefix)
            r.bold = True
        p.add_run(text)
        return p

    def table(rows):
        t = doc.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = "Light Grid Accent 1"
        t.alignment = 1
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                t.cell(i, j).text = val
        return t

    TEN, NGAN, PFX = P["ten"], P["ngan"], P["prefix"]

    # ───────────────────────── BÌA ─────────────────────────
    tp = doc.add_paragraph()
    tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = tp.add_run("MÔ TẢ NGHIỆP VỤ")
    r.bold = True
    r.font.size = Pt(20)
    sp = doc.add_paragraph()
    sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sp.add_run(TEN)
    r.bold = True
    r.font.size = Pt(16)
    ip = doc.add_paragraph()
    ip.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ip.add_run("Phân hệ Bán hàng → Kế hoạch · Redmine %s · Cập nhật ngày %s" % (P["issue"], TODAY))
    doc.add_page_break()

    # ───────────────────────── 1 ─────────────────────────
    h("1. TÀI LIỆU NÀY DÀNH CHO AI", 1)
    para("Tài liệu mô tả nghiệp vụ của màn “%s” trên hệ thống mới: màn dùng để làm gì, nằm ở đâu trong luồng "
         "kế hoạch – chỉ tiêu kinh doanh, ai làm gì ở từng bước, phiếu đi qua những trạng thái nào, ai nhận "
         "thông báo, và các quy tắc bắt buộc. Tài liệu không hướng dẫn bấm từng nút (xem tài liệu Hướng dẫn "
         "sử dụng) và không liệt kê kịch bản kiểm thử (xem file test case cùng thư mục)." % TEN)
    bullet("Nhân viên kinh doanh: hiểu khi nào được lập phiếu, phải nhập gì, gửi cho ai.")
    bullet("Trưởng phòng, trưởng bộ phận, cán bộ quản lý: hiểu mình thấy phiếu nào, duyệt / từ chối / gửi Ban "
           "giám đốc ra sao.")
    bullet("Người nghiệm thu và bộ phận kiểm thử: đối chiếu hệ thống có chạy đúng nghiệp vụ không, biết trước "
           "những điểm cố ý làm khác bản cũ và những giới hạn hiện tại để không báo nhầm lỗi.")

    # ───────────────────────── 2 ─────────────────────────
    h("2. CHỨC NĂNG NÀY DÙNG ĐỂ LÀM GÌ", 1)
    h("2.1. Mục đích", 2)
    para(P["muc_dich"])
    para("Màn hình được chuyển từ phần mềm ERP cũ sang hệ thống mới, giao diện và luật theo bản demo khách hàng "
         "đã chốt. Thay đổi lớn nhất: bỏ tầng khách hàng — nhân viên nhập số thẳng trên dòng Tỉnh/TP, số khách "
         "nhập tay ở ô SL khách.")
    h("2.2. Vị trí trong luồng lớn", 2)
    para("Luồng kế hoạch – chỉ tiêu kinh doanh đi theo thứ tự sau:")
    bullet("Phiếu giao chỉ tiêu kinh doanh theo nhân viên (màn Bán hàng → Kế hoạch → Giao chỉ tiêu kinh doanh → "
           "Theo nhân viên), đã ở trạng thái Đã duyệt — là ĐẦU VÀO bắt buộc. Nó quyết định nhân viên có được lập "
           "kế hoạch không, năm nào lập được và được chọn Tỉnh/TP nào.", "Đầu vào: ")
    bullet("Phiếu %s (màn này) — nhân viên tự lập, trưởng phòng duyệt, gửi Ban giám đốc." % NGAN, "Màn này: ")
    bullet(P["vi_tri_pheu"] + " Nút “%s” trên form dùng hệ số này để điền sẵn số liệu." % P["nut_lay"], "Màn liên quan: ")
    bullet("Kế hoạch của phòng ban / công ty và các báo cáo kế hoạch bên ERP. Các màn này hiện vẫn đọc số theo "
           "từng dòng khách hàng của phiếu cũ, nên CHƯA nhận số của phiếu lập trên hệ thống mới (xem mục 12).",
           "Phía sau: ")
    h("2.3. Giá trị mang lại", 2)
    bullet("Kế hoạch bám đúng địa bàn được giao: chỉ chọn được Tỉnh/TP có trong chỉ tiêu, không lập lan man.")
    bullet("Nhìn thấy ngay kế hoạch so với chỉ tiêu ở từng tỉnh (tab Theo thị trường) mà không phải mở hai màn.")
    bullet("Nhập nhanh: không phải liệt kê từng khách hàng; có thể lấy sẵn số từ kế hoạch kia theo hệ số rồi sửa tay.")
    bullet("Trưởng phòng có danh sách “chờ duyệt” riêng và nhận thông báo ngay khi nhân viên gửi phiếu.")
    bullet("Một nhân viên lập được nhiều phiếu trong một năm (vd lập lại khi được giao thêm chỉ tiêu).")

    # ───────────────────────── 3 ─────────────────────────
    h("3. NHỮNG AI THAM GIA", 1)
    table([
        ["Vai trò", "Làm gì trong nghiệp vụ này"],
        ["Người lập phiếu\n(nhân viên kinh doanh có chỉ tiêu được giao)",
         "Lập phiếu cho CHÍNH MÌNH (không lập hộ người khác), nhập số theo tháng – Tỉnh/TP, có thể lấy dữ liệu từ "
         "kế hoạch kia, lưu, gửi duyệt. Sửa / gửi lại khi phiếu ở Đang tạo (kể cả sau khi bị từ chối). Hủy phiếu "
         "khi còn Đang tạo hoặc Chờ TP duyệt."],
        ["Người duyệt cấp trưởng phòng",
         "Người có quyền “%s” VÀ (được giao quản lý phòng của phiếu, hoặc đang thuộc cùng phòng với phiếu), không "
         "phải người lập. Nhận thông báo khi có phiếu gửi tới; Duyệt hoặc Từ chối (bắt buộc lý do); sau khi duyệt "
         "thì bấm Gửi BGĐ." % P["q_duyet"]],
        ["Trưởng phòng là người lập",
         "Trưởng phòng tự lập phiếu cho mình thì khi gửi, phiếu đi thẳng lên Chờ BGĐ duyệt — không ai duyệt cấp "
         "phòng, không tự duyệt phiếu của mình."],
        ["Trưởng phòng / trưởng bộ phận (quản lý)",
         "Xem phiếu của nhân viên phòng / bộ phận mình quản lý để theo dõi (chỉ xem; muốn duyệt phải có quyền duyệt "
         "như dòng trên)."],
        ["Cán bộ quản lý có quyền xem theo cấp",
         "Có quyền “%s” theo mức Phòng ban / Công ty / Tổng công ty: xem, in, xuất Excel phiếu trong phạm vi đó."
         % P["q_xem"]],
        ["Ban giám đốc",
         "Đích đến cuối của phiếu (Chờ BGĐ duyệt). Màn duyệt của Ban giám đốc CHƯA có trong đợt này (mục 12)."],
        ["Người lập phiếu giao chỉ tiêu",
         "Không thao tác trên màn này, nhưng phiếu giao chỉ tiêu theo nhân viên Đã duyệt của họ là điều kiện để "
         "nhân viên lập được kế hoạch."],
    ])

    # ───────────────────────── 4 ─────────────────────────
    h("4. VÒNG ĐỜI CỦA PHIẾU", 1)
    para("Phiếu có 6 trạng thái (giữ nguyên bộ trạng thái của ERP). Năm trạng thái đầu và Hủy do chính màn này "
         "tạo ra; riêng “BGĐ đã duyệt” hiện chỉ có ở phiếu cũ — màn duyệt của Ban giám đốc chưa làm.")
    table([
        ["Trạng thái (màu nhãn)", "Ý nghĩa", "Ai làm phiếu chuyển sang trạng thái này"],
        ["Đang tạo (xám)", "Phiếu nháp, chỉ người lập nhìn thấy và sửa được.",
         "Người lập bấm “Lưu” khi tạo / sửa; hoặc người duyệt cấp trưởng phòng bấm “Từ chối”."],
        ["Chờ TP duyệt (cam)", "Đã gửi, chờ người duyệt cấp trưởng phòng.",
         "Người lập (không phải trưởng phòng của phòng phiếu) bấm “Lưu và gửi” hoặc “Gửi duyệt”."],
        ["TP đã duyệt (xanh dương)", "Cấp phòng đã đồng ý, chờ gửi lên Ban giám đốc.",
         "Người duyệt cấp trưởng phòng bấm “Duyệt”."],
        ["Chờ BGĐ duyệt (cam)", "Đã lên Ban giám đốc, chờ duyệt cuối.",
         "Người duyệt cấp trưởng phòng bấm “Gửi BGĐ”; hoặc trưởng phòng tự lập phiếu rồi gửi (đi thẳng)."],
        ["BGĐ đã duyệt (xanh lá)", "Phiếu đã duyệt cuối cùng.",
         "Chưa phát sinh từ màn này. Phiếu cũ có trạng thái này là do duyệt kế hoạch phòng ban bên ERP cập nhật "
         "ngược về."],
        ["Hủy (đỏ)", "Phiếu bỏ, không sửa, không in, không xuất Excel; vẫn xem được.",
         "Người lập bấm “Hủy phiếu” khi phiếu ở Đang tạo hoặc Chờ TP duyệt."],
    ])
    para("Không có thao tác Xóa phiếu: phiếu không dùng nữa thì Hủy. Không có “Hủy duyệt”: phiếu đã TP duyệt "
         "không trả về được Đang tạo trên hệ thống mới.")

    # ───────────────────────── 5 ─────────────────────────
    h("5. LUỒNG HOẠT ĐỘNG CHI TIẾT", 1)

    h("5.1. Điều kiện trước — có chỉ tiêu được giao", 2)
    para("Nhân viên chỉ lập được phiếu khi đã có ít nhất một phiếu giao chỉ tiêu kinh doanh theo nhân viên ở "
         "trạng thái Đã duyệt, trong đó có dòng chỉ tiêu mang tên mình, cho năm hiện tại hoặc các năm sau. Chưa có "
         "thì bấm “Tạo mới” hệ thống hiện hộp thoại “Chưa thể lập %s”: “Tài khoản của bạn chưa có phiếu giao chỉ "
         "tiêu kinh doanh Đã duyệt cho năm <năm nay> trở đi nên chưa thể lập %s. Vui lòng liên hệ trưởng phòng để "
         "được giao chỉ tiêu.” — form không mở." % (NGAN, NGAN))
    para("Chỉ tiêu của một Tỉnh/TP = tổng các dòng chỉ tiêu của nhân viên ở tỉnh đó trên mọi phiếu giao chỉ tiêu Đã "
         "duyệt cùng năm, cộng gộp hai nhóm khách (khách hãng và khách khác), tách riêng hàng hóa / dịch vụ, mỗi "
         "nhóm gồm số khách và doanh số. Phần chỉ tiêu giao cho “nhân viên mới” chưa gắn tài khoản thì không ai lập "
         "kế hoạch được — trưởng phòng phải sửa phiếu giao chỉ tiêu để gắn phần đó vào một tài khoản.")

    h("5.2. Bước 1 — Lập phiếu", 2)
    para("Người lập vào màn danh sách, bấm “Tạo mới”. Form gồm hai khối:")
    bullet("“Thông tin phiếu”: ô Năm (bắt buộc; chọn từ năm nay tới năm nay + 4; mặc định là năm sớm nhất có chỉ "
           "tiêu) và ô Nhân viên — luôn là tài khoản đang lập, chỉ đọc, hiển thị “Tên - Mã phòng - Mã nhân viên”.")
    bullet("“Chi tiết”: bảng cây Tháng → Tỉnh/TP. Năm lập phiếu là năm hiện tại thì có các tháng từ tháng lập "
           "phiếu tới tháng 12; năm sau thì đủ 12 tháng. Mỗi tháng có sẵn một dòng Tỉnh/TP trống, bấm “Thêm Tỉnh/TP” "
           "để thêm dòng, nút thùng rác để xoá dòng (dòng đã có số thì hỏi lại trước khi xoá).")
    para("Trên mỗi dòng Tỉnh/TP, người lập chọn tỉnh (chỉ tỉnh có trong chỉ tiêu của năm, mỗi tỉnh một dòng trong "
         "một tháng) rồi nhập các cột số:")
    table([["Cột", "Ý nghĩa", "Bắt buộc"]] + P["cot"])
    para("Bảng có 3 tab, cùng một bộ số nhưng nhìn theo 3 cách:")
    table([
        ["Tab", "Cách xếp", "Dùng để"],
        ["Chi tiết theo tháng", "Tháng (số La Mã) → Tỉnh/TP theo thứ tự đã nhập. Tab DUY NHẤT nhập được số. "
         "Có ô chọn cấp hiển thị “Chỉ Tháng / Đến Tỉnh/TP” và thu / mở từng tháng.", "Lập và sửa kế hoạch."],
        ["Theo thị trường", "Tỉnh/TP → Tháng, gồm cả tỉnh có chỉ tiêu nhưng chưa lập kế hoạch. Chỉ xem.",
         "So kế hoạch với chỉ tiêu được giao. " + P["chi_tieu_hien"]],
        ["Theo tháng", "Tháng → Tỉnh/TP theo thứ tự tỉnh. Chỉ xem.", "Xem tổng từng tháng."],
    ])
    para("Dòng TỔNG luôn ghim ở đầu bảng, ghi “<tên nhân viên> - N khách - M thị trường” (N = tổng SL khách, M = số "
         "Tỉnh/TP khác nhau đã lập). Mỗi dòng tháng ghi “Tháng X (N khách)”. So sánh với chỉ tiêu chỉ để nhìn, "
         "KHÔNG chặn lưu hay gửi.")
    para("Kết thúc bước này người lập bấm “Lưu” (phiếu ở Đang tạo, làm tiếp sau) hoặc “Lưu và gửi” (lưu rồi gửi "
         "ngay — xem bước 2). Lưu xong hệ thống quay về màn danh sách. Rời form khi chưa lưu thì hệ thống hỏi lại.")

    h("5.3. Tùy chọn — Lấy dữ liệu từ %s" % P["kia_ngan"], 2)
    para("Trên form Tạo mới / Sửa (khi năm đang chọn có chỉ tiêu) có nút “%s”. Bấm vào mở hộp thoại cùng tên:"
         % P["nut_lay"])
    bullet("Chọn “Phiếu nguồn”: chỉ liệt kê phiếu %s CỦA CHÍNH TÀI KHOẢN, cùng năm với phiếu đang lập, đã ở TP đã "
           "duyệt hoặc BGĐ đã duyệt, phiếu duyệt gần nhất đứng đầu. Phiếu cũ lập trên ERP cũng lấy được. Không có "
           "phiếu nào thì hộp thoại ghi “Chưa có phiếu %s đã duyệt năm <năm>”." % (P["kia"].lower(), P["kia_ngan"]))
    bullet("Nhập “Hệ số chuyển đổi (báo giá ÷ hệ số = hợp đồng)”: số nguyên từ 1 đến 99, mặc định 3. Nhập 0, để "
           "trống hay nhập ngoài khoảng thì báo đỏ “Hệ số là số nguyên từ 1 đến 99” ngay dưới ô và ẩn nút Áp dụng.")
    bullet("Hệ thống tính sẵn và hiện bảng xem trước (Tháng · Tỉnh/TP · các số sẽ điền + dòng Tổng), kèm dòng tóm "
           "tắt “Sẽ điền N tháng · M dòng tỉnh”. Phiếu đích là %s nên số được %s cho hệ số:" % (NGAN, P["huong"]))
    table([["Ô của phiếu đang lập", "Cách tính từ phiếu nguồn"]] + P["quy_doi"])
    para("Ví dụ: " + P["vi_du"])
    bullet("Giữ nguyên tháng và Tỉnh/TP của phiếu nguồn, nhưng BỎ các tháng trước tháng bắt đầu của phiếu đang lập "
           "và các Tỉnh/TP không có trong chỉ tiêu; hộp thoại ghi rõ đã bỏ bao nhiêu tháng / dòng. Bỏ hết thì báo "
           "“Không còn tháng / tỉnh nào để điền” và không cho Áp dụng.")
    bullet("Bấm “Áp dụng”: nếu form đang có số, hệ thống hỏi “Ghi đè dữ liệu đang nhập?” — đồng ý thì THAY TOÀN BỘ "
           "bảng bằng dữ liệu mới (không cộng dồn). Sau đó vẫn sửa tay được; số chỉ được ghi khi người lập bấm Lưu.")
    bullet("Phiếu đang lập không lưu lại đã lấy từ phiếu nào, hệ số bao nhiêu.")

    h("5.4. Bước 2 — Gửi duyệt", 2)
    para("Người lập bấm “Lưu và gửi” trên form, hoặc “Gửi duyệt” (có hộp xác nhận) ở màn Chi tiết / dòng danh "
         "sách. Điều kiện: %s, nếu không hệ thống báo “%s”. Hệ thống rẽ hai hướng:" % (P["dk_gui"], P["loi_gui"]))
    table([
        ["Người lập là ai", "Diễn ra thế nào", "Kết quả"],
        ["Nhân viên (không phải trưởng phòng của phòng phiếu)",
         "Phiếu chuyển sang Chờ TP duyệt, ghi lại thời điểm gửi.",
         "Người duyệt cấp trưởng phòng nhận thông báo “Gửi duyệt” (mục 6). Phiếu khóa, người lập không sửa được nữa."],
        ["Trưởng phòng (người được giao quản lý đúng phòng của phiếu)",
         "Bỏ qua cấp phòng, phiếu chuyển thẳng sang Chờ BGĐ duyệt.",
         "Không ai nhận thông báo (Ban giám đốc chưa có màn duyệt). Phiếu khóa."],
    ])

    h("5.5. Bước 3 — Trưởng phòng duyệt hoặc từ chối", 2)
    para("Người duyệt mở phiếu từ thông báo, từ lối vào “chờ duyệt” hoặc từ danh sách. Ở dòng danh sách, nút "
         "“Duyệt” chỉ mở màn Chi tiết của phiếu; việc duyệt / từ chối làm ở màn Chi tiết sau khi xem đủ 3 tab.")
    table([
        ["Hướng xử lý", "Diễn ra thế nào", "Kết quả"],
        ["Duyệt", "Bấm “Duyệt”, xác nhận.",
         "Phiếu sang TP đã duyệt, ghi người duyệt + ngày duyệt. Người lập nhận thông báo “Đã duyệt”."],
        ["Từ chối", "Bấm “Từ chối”, BẮT BUỘC nhập Lý do (tối đa 255 ký tự) rồi xác nhận.",
         "Phiếu về Đang tạo, lý do hiện ở đầu phiếu (“Lý do từ chối: …”). Người lập nhận thông báo kèm lý do, sửa rồi "
         "gửi lại được, số phiếu giữ nguyên. Người duyệt không còn thấy phiếu cho tới khi được gửi lại."],
    ])

    h("5.6. Bước 4 — Gửi Ban giám đốc", 2)
    para("Với phiếu TP đã duyệt, người duyệt cấp trưởng phòng bấm “Gửi BGĐ” (ở dòng danh sách hoặc màn Chi tiết, "
         "có hộp xác nhận). Phiếu sang Chờ BGĐ duyệt; người lập nhận thông báo “Gửi BGĐ”. Từ đây phiếu dừng lại cho "
         "tới khi có màn duyệt của Ban giám đốc (mục 12).")

    h("5.7. Hủy phiếu", 2)
    para("Người lập bấm “Hủy phiếu” (hộp xác nhận “Phiếu Hủy không sửa được.”) khi phiếu đang Đang tạo hoặc Chờ TP "
         "duyệt. Phiếu sang Hủy, vẫn hiện trong danh sách để tra cứu, không in, không xuất Excel được. Không có "
         "thông báo cho ai, kể cả khi người duyệt đang chờ duyệt phiếu đó.")

    h("5.8. Phiếu cũ lập trên ERP", 2)
    para("Phiếu lập trước đây trên ERP (có chi tiết từng khách hàng) vẫn hiện trong danh sách như phiếu thường, "
         "nhưng CHỈ được Xem, In, Xuất Excel và xem Lịch sử — mọi nút Sửa, Gửi duyệt, Duyệt, Từ chối, Gửi BGĐ, Hủy "
         "đều ẩn, kể cả khi phiếu cũ đang Đang tạo hay Chờ TP duyệt. Màn Chi tiết ghi “Phiếu lập trên ERP (có chi "
         "tiết khách hàng) — chỉ xem. SL khách = số khách hàng của từng dòng Tỉnh/TP.” Số liệu hiện ở tầng Tỉnh/TP; "
         "SL khách là số khách hàng khác nhau của dòng tỉnh đó. Phiếu cũ lập cho “Nhân viên mới …” hiện đúng tên "
         "đã ghi trên phiếu. Phiếu cũ không xuất hiện ở lối vào “chờ duyệt”.")

    # ───────────────────────── 6 ─────────────────────────
    h("6. THÔNG BÁO — AI NHẬN, KHI NÀO, NỘI DUNG GÌ", 1)
    para("Thông báo hiện ở chuông thông báo trên thanh công cụ (và thông báo đẩy trên ứng dụng điện thoại). Có "
         "đúng bốn sự kiện phát sinh thông báo; tiền tố của màn này là [%s]." % PFX)
    table([
        ["Sự kiện", "Ai nhận", "Nội dung thông báo", "Bấm vào thì đi đâu"],
        ["Phiếu được gửi duyệt (người lập không phải trưởng phòng của phòng phiếu)",
         "Những người có quyền “%s” ở công ty của phiếu VÀ (được giao quản lý phòng của phiếu, hoặc đang thuộc cùng "
         "phòng của phiếu); trừ người lập. KHÔNG phải toàn bộ nhân viên phòng." % P["q_duyet"],
         "[%s] Gửi duyệt: <số phiếu>" % PFX,
         "Mở thẳng màn Chi tiết của đúng phiếu đó (có nút Duyệt / Từ chối)."],
        ["Người duyệt cấp trưởng phòng bấm Duyệt", "Người lập phiếu (một người).",
         "[%s] Đã duyệt: <số phiếu>" % PFX, "Mở thẳng màn Chi tiết của phiếu."],
        ["Người duyệt cấp trưởng phòng bấm Từ chối", "Người lập phiếu (một người).",
         "[%s] Từ chối: <số phiếu>. Lý do: <lý do từ chối>" % PFX,
         "Mở thẳng màn Chi tiết của phiếu (lý do hiện ở đầu phiếu, có nút Sửa)."],
        ["Người duyệt cấp trưởng phòng bấm Gửi BGĐ", "Người lập phiếu (một người). Ban giám đốc CHƯA nhận.",
         "[%s] Gửi BGĐ: <số phiếu>" % PFX, "Mở thẳng màn Chi tiết của phiếu."],
    ])
    para("Quy ước chung về thông báo:")
    bullet("Số phiếu được in đậm. Cả câu tối đa 180 ký tự; quá dài thì cắt phần lý do ở cuối, bản đầy đủ xem bằng "
           "“Xem thêm”.")
    bullet("Người lập không tự nhận thông báo “Gửi duyệt” của chính mình dù có quyền duyệt và cùng phòng. Một người "
           "vừa quản lý phòng vừa ngồi cùng phòng chỉ nhận một thông báo.")
    bullet("Không ai có quyền duyệt ở phòng đó thì không ai nhận thông báo “Gửi duyệt” và cũng không ai duyệt được — "
           "phải cấp quyền “%s” cho trưởng phòng trước." % P["q_duyet"])
    bullet("Lỗi gửi thông báo không làm hỏng nghiệp vụ: phiếu vẫn lưu và đổi trạng thái bình thường.")
    para("Các sự kiện KHÔNG phát sinh thông báo (cố ý, QA không báo thiếu):")
    bullet("Lưu phiếu (tạo / sửa).")
    bullet("Trưởng phòng tự lập phiếu rồi gửi — phiếu đi thẳng Chờ BGĐ duyệt, không báo ai.")
    bullet("Gửi BGĐ: không báo Ban giám đốc (chưa có màn đích để mở).")
    bullet("Hủy phiếu, kể cả khi phiếu đang Chờ TP duyệt — người duyệt không được báo (xem mục 12).")
    bullet("Mọi thao tác với phiếu cũ (chỉ xem nên không có thao tác đổi trạng thái).")

    # ───────────────────────── 7 ─────────────────────────
    h("7. PHÂN QUYỀN — AI THẤY GÌ, AI LÀM ĐƯỢC GÌ", 1)
    para("Màn này dùng đúng hai quyền: “%s” (có phạm vi Phòng ban / Công ty / Tổng công ty) và “%s”. Lập phiếu "
         "KHÔNG cần quyền — chỉ cần có chỉ tiêu được giao." % (P["q_xem"], P["q_duyet"]))
    h("7.1. Quyền nhìn thấy dữ liệu", 2)
    para("Một người thấy một phiếu nếu thoả MỘT trong các dòng dưới đây (cộng dồn):")
    table([
        ["Quyền / vai trò", "Nhìn thấy những phiếu nào"],
        ["Mọi người dùng", "Phiếu do chính mình lập (kể cả Đang tạo)."],
        ["“%s” — mức Tổng công ty" % P["q_xem"], "Phiếu của mọi công ty."],
        ["“%s” — mức Công ty" % P["q_xem"], "Phiếu của công ty đang thao tác."],
        ["“%s” — mức Phòng ban" % P["q_xem"], "Phiếu của phòng mình đang thuộc và các phòng mình được giao quản lý."],
        ["Trưởng phòng (được giao quản lý phòng — không cần quyền)", "Mọi phiếu của phòng mình quản lý."],
        ["Trưởng bộ phận (được giao quản lý bộ phận — không cần quyền)",
         "Phiếu của nhân viên thuộc bộ phận mình quản lý (chỉ xem)."],
        ["“%s”" % P["q_duyet"],
         "Phiếu Chờ TP duyệt của phòng mình duyệt được (phòng mình quản lý hoặc phòng mình đang thuộc)."],
        ["Người đã duyệt phiếu", "Phiếu mình đã duyệt (cấp trưởng phòng hoặc Ban giám đốc)."],
        ["(Không có quyền nào, không quản lý phòng / bộ phận nào)",
         "Vẫn vào được màn, nhưng chỉ thấy phiếu do chính mình lập."],
    ])
    para("Hai quy tắc luôn đúng, không phụ thuộc quyền:")
    bullet("Phiếu Đang tạo (kể cả phiếu vừa bị từ chối) chỉ người lập nhìn thấy — kể cả người có quyền xem Tổng "
           "công ty cũng không thấy.")
    bullet("“Phòng của phiếu” là phòng / bộ phận của người lập TẠI THỜI ĐIỂM LẬP, ghi luôn trên phiếu. Người lập "
           "chuyển phòng sau đó thì phiếu vẫn thuộc phòng cũ và do người duyệt của phòng cũ xử lý.")
    para("Người “thấy phiếu của người khác” (có quyền xem, có quyền duyệt hoặc đang quản lý phòng / bộ phận) được "
         "coi là cấp trên: danh sách hiện cột Nhân viên và có đủ bộ lọc (mục 10). Người chỉ thấy phiếu của mình thì "
         "danh sách hiện cột Năm, ẩn cột Nhân viên.")

    h("7.2. Quyền thao tác", 2)
    table([
        ["Thao tác", "Điều kiện được phép"],
        ["Tạo mới", "Có phiếu giao chỉ tiêu theo nhân viên Đã duyệt cho năm nay trở đi (mục 5.1). Không cần quyền."],
        ["Sửa · Gửi duyệt · Lấy dữ liệu từ %s" % P["kia_ngan"],
         "Phiếu ở Đang tạo, do chính mình lập, lập trên hệ thống mới."],
        ["Duyệt · Từ chối",
         "Có quyền “%s” VÀ (được giao quản lý phòng của phiếu, hoặc đang thuộc cùng phòng); không phải người lập; "
         "phiếu ở Chờ TP duyệt; phiếu lập trên hệ thống mới. Từ chối chỉ có ở màn Chi tiết." % P["q_duyet"]],
        ["Gửi BGĐ", "Cùng nhóm người như Duyệt; phiếu ở TP đã duyệt."],
        ["Hủy phiếu", "Người lập; phiếu ở Đang tạo hoặc Chờ TP duyệt; phiếu lập trên hệ thống mới."],
        ["In (3 kiểu) · Xuất Excel 1 phiếu", "Ai xem được phiếu; phiếu không ở trạng thái Hủy."],
        ["Lịch sử", "Ai xem được phiếu."],
        ["Xuất Excel danh sách", "Ai vào được màn; xuất đúng các phiếu mình đang thấy."],
    ])
    para("Nút nào không đủ điều kiện thì ẨN HẲN, không hiện dạng mờ. Cùng một phiếu, nút ở dòng danh sách và ở "
         "màn Chi tiết giống nhau, trừ hai điểm: “Duyệt” ở danh sách chỉ dẫn sang màn Chi tiết, và “Từ chối” chỉ có "
         "ở màn Chi tiết. Hệ thống kiểm lại điều kiện ở máy chủ, nên mở thẳng đường dẫn Sửa hay gửi thao tác khi "
         "không đủ điều kiện vẫn bị chặn.")

    # ───────────────────────── 8 ─────────────────────────
    h("8. QUY TẮC NGHIỆP VỤ BẮT BUỘC", 1)
    h("8.1. Bắt buộc nhập — theo từng nút bấm", 2)
    table([
        ["Khi bấm", "Bắt buộc phải có"],
        ["Lưu",
         "Năm (và năm đó phải có chỉ tiêu được giao). Với từng dòng: dòng có số thì phải chọn Tỉnh/TP; dòng đã chọn "
         "Tỉnh/TP thì phải có SL khách; trong từng nhóm hàng hóa / dịch vụ, cặp số lượng ↔ doanh số (giá trị) phải "
         "đi cùng nhau. Phiếu chưa có dòng nào vẫn lưu được."],
        ["Lưu và gửi · Gửi duyệt", "Như Lưu, cộng thêm: " + P["dk_gui"] + "."],
        ["Từ chối", "Lý do (tối đa 255 ký tự)."],
        ["Duyệt · Gửi BGĐ · Hủy phiếu", "Chỉ cần xác nhận."],
    ])
    para("Thiếu thì ô lỗi viền đỏ, câu “Bắt buộc phải nhập” ngay dưới ô, hệ thống chuyển về tab Chi tiết theo "
         "tháng, mở tháng có lỗi và cuộn tới ô lỗi đầu tiên; số người dùng đã gõ được giữ nguyên.")

    h("8.2. Ràng buộc dữ liệu", 2)
    bullet("Tỉnh/TP chỉ chọn trong chỉ tiêu được giao của năm phiếu; một tỉnh chỉ một dòng trong một tháng (trùng "
           "báo “Tỉnh/TP đã có trong tháng này”). Tỉnh đã lập nay không còn trong chỉ tiêu (chỉ tiêu bị sửa) vẫn hiện "
           "để sửa.")
    bullet("Tháng: năm hiện tại tính từ tháng lập phiếu tới tháng 12; năm sau đủ 12 tháng. Mở Sửa sau này vẫn tính "
           "theo ngày lập phiếu, không theo ngày mở.")
    bullet("Ô số: số nguyên không âm, tối đa 15 chữ số, hiển thị dạng 1,234,567. Ô bằng 0 để trống. Hệ thống không "
           "tự sửa số người dùng gõ.")
    bullet("Khi lưu: dòng trống hoàn toàn và tháng không còn dòng nào bị bỏ; số của tháng và của cả phiếu do hệ thống "
           "tự cộng từ các dòng Tỉnh/TP.")
    bullet("Đổi Năm khi đã nhập số: hỏi “Đổi năm? Số liệu theo tháng đã nhập sẽ mất.” — đồng ý thì bảng dựng lại "
           "theo chỉ tiêu của năm mới.")
    bullet("Một nhân viên lập được nhiều phiếu trong cùng một năm.")

    h("8.3. Chỉ tiêu dùng để so sánh — luôn lấy bản mới nhất", 2)
    para("Chỉ tiêu hiển thị ở tab Theo thị trường là chỉ tiêu Đã duyệt HIỆN TẠI của nhân viên ghi trên phiếu (không "
         "chụp lại lúc lập). Phiếu giao chỉ tiêu được sửa / duyệt lại thì con số so sánh trên phiếu kế hoạch cũng "
         "đổi theo. Năm không còn chỉ tiêu nào (chỉ tiêu bị hủy duyệt) thì không lưu được phiếu của năm đó.")

    h("8.4. Khóa chỉnh sửa", 2)
    bullet("Chỉ phiếu Đang tạo, do chính mình lập trên hệ thống mới mới sửa được. Rời Đang tạo là khóa — kể cả mở "
           "thẳng đường dẫn Sửa cũng bị đưa về màn Chi tiết.")
    bullet("Muốn sửa phiếu đã gửi: người duyệt phải Từ chối để trả về Đang tạo. Phiếu đã TP duyệt thì không trả về "
           "được (không có Hủy duyệt).")
    bullet("Phiếu Hủy và phiếu cũ lập trên ERP: chỉ xem.")

    h("8.5. Danh mục bị khóa", 2)
    para("Ô lọc Công ty / Phòng ban ở danh sách vẫn liệt kê công ty, phòng ban đã khóa nếu còn phiếu thuộc về nó "
         "(có biểu tượng ổ khóa trước tên), để tra cứu phiếu cũ không bị mất.")

    h("8.6. Số phiếu", 2)
    para("Số phiếu do hệ thống cấp ngay ở lần lưu đầu tiên, dạng <mã công ty>_%s_<năm>.<5 chữ số>, ví dụ "
         "TPE_%s_2026.00123. Năm trong số phiếu là năm kế hoạch; nếu khi sửa người lập đổi Năm thì phần năm trong số "
         "phiếu đổi theo, phần số giữ nguyên. Phiếu cũ giữ nguyên số đã có trên ERP (khuôn khác nên không trùng)."
         % (PFX, PFX))

    # ───────────────────────── 9 ─────────────────────────
    h("9. CÁC LỐI VÀO MÀN HÌNH", 1)
    para("Màn có một đường dẫn chính và một lối vào “chờ duyệt” (cùng màn, khác danh sách hiện ra). Đường dẫn đầy "
         "đủ là địa chỉ hệ thống mới ghép với phần ở cột Đường dẫn.")
    t9 = table([
        ["Bấm vào đâu (phân hệ → nhóm → mục)", "Đường dẫn", "Danh sách hiện ra", "Dùng khi nào"],
        ["Hệ thống mới: " + P["menu"], P["path"],
         "Toàn bộ phiếu trong phạm vi xem của tôi (mục 7.1). Có nút Tạo mới.",
         "Lối vào chính: lập phiếu, theo dõi phiếu của mình và của cấp dưới."],
        ["Hệ thống mới: " + P["menu_duyet"] + " (mục chỉ hiện với người có quyền “%s”)" % P["q_duyet"],
         P["path"] + "?type=for-approve",
         "Chỉ phiếu Chờ TP duyệt và TP đã duyệt của phòng tôi duyệt được, trừ phiếu tôi tự lập và phiếu cũ. Không có "
         "nút Tạo mới, không có ô lọc Trạng thái.",
         "Danh sách việc cần duyệt / cần gửi Ban giám đốc."],
        ["ERP: " + P["erp_menu"] + " (mở tab mới sang hệ thống mới)", P["path"],
         "Như dòng lối vào chính.", "Người quen dùng menu ERP."],
        ["ERP: " + P["erp_menu_duyet"] + " (mở tab mới; chỉ hiện với người có quyền duyệt)",
         P["path"] + "?type=for-approve", "Như dòng chờ duyệt ở trên.", "Người duyệt quen dùng menu ERP."],
        ["(Không có mục menu — bấm vào thông báo trên chuông)", P["path"] + "/<số định danh phiếu>",
         "Mở thẳng màn Chi tiết của một phiếu.", "Xử lý ngay phiếu vừa được báo."],
    ])
    path_tables.append(t9)
    para("Ba điều cần biết:")
    bullet("Đường dẫn quyết định PHẠM VI danh sách, không thay quyền: người không có quyền duyệt mà mở đường dẫn "
           "“chờ duyệt” thì danh sách trống.")
    bullet("Nút Làm mới chỉ xoá điều kiện lọc, không đưa người dùng sang lối vào khác.")
    bullet("Đường dẫn kèm giá trị lạ thì hệ thống bỏ qua, giữ phạm vi của lối vào chính.")
    para("Menu lập / danh sách / chờ duyệt cũ của màn này bên ERP đã đổi thành link sang hệ thống mới; ERP không còn "
         "chỗ lập phiếu kiểu cũ trên menu.")

    # ───────────────────────── 10 ─────────────────────────
    h("10. TRA CỨU, IN VÀ XUẤT DỮ LIỆU", 1)
    bullet("Tìm nhanh: một ô “Tìm theo số phiếu, nhân viên”.")
    bullet("Bộ lọc nâng cao — người chỉ thấy phiếu của mình: Năm · Người duyệt · Trạng thái. Cấp trên: Công ty (chỉ "
           "khi xem được mọi công ty) · Phòng ban · Bộ phận · Nhân viên · Năm · Người duyệt · Trạng thái. Chọn xong tự "
           "lọc. Lối vào chờ duyệt không có ô Trạng thái.")
    bullet("Cột danh sách: STT · Số phiếu (bấm để xem) · Năm · Nhân viên · Bộ phận (ẩn sẵn) · Phòng ban (ẩn sẵn) · "
           "%s · Người lập (ẩn sẵn) · Ngày lập · Người duyệt · Ngày duyệt (ẩn sẵn) · Trạng thái · Hành động. Người "
           "duyệt / Ngày duyệt là lần duyệt gần nhất (Ban giám đốc nếu có, không thì trưởng phòng). Bật / tắt cột "
           "bằng nút cấu hình cột, hệ thống nhớ cho lần sau. Mặc định xếp ngày lập mới nhất lên đầu." % P["cot_ds"])
    bullet("In: ba kiểu “In chi tiết”, “In theo thị trường”, “In theo tháng” (ở dòng danh sách); ở màn Chi tiết nút "
           "“In” in theo tab đang mở. Bản in khổ A4 ngang, đầu trang là tiêu đề thư của công ty ghi trên phiếu, số "
           "phiếu, ngày lập, tiêu đề “%s”, dòng Năm · Nhân viên · Phòng ban · Trạng thái, bảng số và khối ký Người lập "
           "· Trưởng phòng · Ban giám đốc (có tên, ngày khi đã duyệt). Phiếu Hủy không in được." % TEN.upper())
    bullet("Xuất Excel 1 phiếu: một file gồm 3 trang tính tương ứng 3 tab (Chi tiết theo tháng · Theo thị trường · "
           "Theo tháng), ô số là số thật để cộng trừ được.")
    bullet("Xuất Excel danh sách: nút Xuất Excel trên thanh công cụ, chọn được cột cần xuất, xuất đúng bộ lọc đang "
           "áp dụng, có dòng báo tiến độ khi dữ liệu lớn.")
    bullet("Lịch sử: menu “Lịch sử” ở dòng danh sách và khối Lịch sử ở cuối màn Chi tiết — ghi tạo mới, mỗi lần lưu, "
           "gửi duyệt, duyệt, từ chối (kèm lý do), gửi BGĐ, hủy.")

    # ───────────────────────── 11 ─────────────────────────
    h("11. LIÊN THÔNG VỚI HỆ THỐNG KHÁC", 1)
    para("Màn này dùng CHUNG dữ liệu phiếu với ERP (cùng một kho dữ liệu sau khi gộp): phiếu cũ của ERP hiện ngay "
         "trên hệ thống mới, phiếu mới lưu vào cùng nơi đó. Chỉ tiêu lấy trực tiếp từ màn Phiếu giao chỉ tiêu kinh "
         "doanh theo nhân viên; danh mục Tỉnh/TP, phòng ban, nhân viên dùng chung. Phiếu lập trên hệ thống mới chưa "
         "được gom vào kế hoạch phòng ban / công ty và các báo cáo kế hoạch bên ERP (mục 12).")
    para("Các điểm cố ý làm khác bản ERP:")
    table([
        ["Điểm khác", "ERP cũ", "Hệ thống mới", "Lý do"],
        ["Tầng khách hàng", "Kế hoạch đi tới từng khách hàng / người liên hệ; số khách do hệ thống đếm.",
         "Bỏ tầng khách hàng; nhập số ở dòng Tỉnh/TP, SL khách nhập tay và bắt buộc.",
         "Theo bản demo khách chốt: nhập nhanh, kế hoạch ở mức địa bàn."],
    ] + P["khac_rieng"] + [
        ["Số phiếu / nhân viên / năm", "Mỗi nhân viên chỉ một phiếu một năm.", "Lập được nhiều phiếu một năm.",
         "Theo bản demo khách chốt."],
        ["Người được lập", "Lập được cho nhân viên khác, kể cả “Nhân viên mới”.",
         "Phiếu luôn của chính tài khoản lập.", "Ai lập người đó chịu trách nhiệm; phần chỉ tiêu của nhân viên mới do "
         "trưởng phòng gắn vào tài khoản qua phiếu giao chỉ tiêu."],
        ["Phạm vi xem", "Theo quyền xem theo cấp.",
         "Quyền xem theo cấp CỘNG vai trò: trưởng phòng thấy phòng mình quản lý, trưởng bộ phận thấy bộ phận, người "
         "duyệt thấy phiếu mình duyệt / chờ mình duyệt.", "Quyết định đã chốt 14/11/2026."],
        ["Phiếu do trưởng phòng lập", "Đi qua bước duyệt cấp phòng.", "Gửi là lên thẳng Chờ BGĐ duyệt.",
         "Không tự duyệt phiếu của mình (theo demo)."],
        ["Lên Ban giám đốc", "Phiếu lên Ban giám đốc qua kế hoạch phòng ban.",
         "Nút “Gửi BGĐ” ngay trên phiếu TP đã duyệt.", "Theo bản demo khách chốt."],
        ["Lấy dữ liệu chéo", "Không có.", "Nút “%s” theo hệ số chuyển đổi." % P["nut_lay"],
         "Hai kế hoạch là hai đầu của cùng một phễu, đỡ nhập hai lần."],
        ["Cách xem / in", "Xem theo tháng → tỉnh → khách hàng.",
         "3 tab (Chi tiết theo tháng · Theo thị trường · Theo tháng), in 3 kiểu A4 ngang, xuất Excel 3 trang tính.",
         "Theo bản demo khách chốt."],
        ["Bỏ phiếu", "Xóa phiếu.", "Không xóa; dùng “Hủy phiếu” (người lập, khi Đang tạo / Chờ TP duyệt).",
         "Giữ dấu vết phiếu."],
        ["Hủy duyệt cấp phòng", "Có (phiếu đã duyệt trả về Đang tạo).", "Không có.", "Bản demo không có; tạm không làm."],
        ["Số phiếu", "Đánh số chung, không có năm.", "Có năm kế hoạch trong số phiếu.", "Theo khuôn phiếu giao chỉ tiêu."],
        ["Phiếu cũ", "Sửa / duyệt bình thường.", "Chỉ xem / in / xuất Excel.", "Phiếu cũ có tầng khách hàng, không "
         "chuyển đổi (quyết định đã chốt)."],
    ])

    # ───────────────────────── 12 ─────────────────────────
    h("12. GIỚI HẠN HIỆN TẠI", 1)
    para("Ngoài phạm vi đợt này (đã chốt với người dùng):")
    bullet("Chưa có màn duyệt của Ban giám đốc: phiếu dừng ở Chờ BGĐ duyệt; Ban giám đốc không nhận thông báo; phiếu "
           "mới chưa lên được BGĐ đã duyệt. Sẽ nối khi làm hộp “Chờ duyệt” tập trung.")
    bullet("Kế hoạch phòng ban / công ty và khoảng 16 báo cáo kế hoạch bên ERP vẫn đọc số theo từng dòng khách hàng "
           "của phiếu cũ, nên phiếu lập trên hệ thống mới hiện RA SỐ 0 ở các màn đó. Sửa ở đợt sau.")
    bullet("Phiếu cũ lập trên ERP chỉ xem; phiếu cũ còn dở dang (Đang tạo / Chờ TP duyệt / TP đã duyệt) không đi "
           "tiếp được trên hệ thống mới. Muốn lập lại thì lập phiếu mới.")
    bullet("Không có Hủy duyệt cấp phòng. Trưởng phòng muốn nhân viên sửa phiếu đã duyệt thì chưa có cách trên hệ "
           "thống mới — nên Từ chối thay vì Duyệt nếu còn cần sửa.")
    para("Các điểm hệ thống hiện chạy khác thiết kế (đã ghi trong test case, chờ quyết định sửa):")
    bullet("Người có quyền duyệt ngồi cùng phòng (không quản lý phòng, không có quyền xem) thấy phiếu TP đã duyệt "
           "trong danh sách “chờ duyệt” kèm nút Gửi BGĐ, nhưng nếu phiếu do người khác duyệt thì bấm Xem bị đưa về "
           "danh sách, bấm Gửi BGĐ bị báo phiếu không tồn tại hoặc không có quyền xem. Cách tạm: để chính người đã "
           "duyệt bấm Gửi BGĐ.")
    bullet("Lịch sử ghi một dòng “Thay đổi thông tin” mỗi lần bấm Lưu, kể cả khi không đổi gì.")
    bullet("Hủy phiếu khi đang Chờ TP duyệt không báo cho người duyệt.")
    bullet("Từ chối chỉ có ở màn Chi tiết; dòng danh sách không có nút Từ chối.")
    bullet("Nút Tạo mới luôn hiện ở lối vào chính, kể cả người chưa có chỉ tiêu (bấm vào mới báo chưa thể lập).")
    bullet("Xuất Excel 1 phiếu luôn ra đủ 3 trang tính, không theo tab đang chọn.")
    bullet("Mở Sửa phiếu của năm không còn chỉ tiêu: bảng số không hiện mà thay bằng dòng “Chưa có phiếu giao chỉ "
           "tiêu Đã duyệt cho năm … — không có Tỉnh/TP để lập kế hoạch”; muốn xem số thì mở màn Chi tiết.")
    bullet("Ô tìm nhanh gõ ký tự % hoặc _ thì ra toàn bộ (hoặc khớp sai) thay vì chỉ phiếu chứa ký tự đó.")

    doc.save(out)
    return out, path_tables


# ───────────────────────── Kiểm thuật ngữ code (theo tc_engine.check_terms, mở rộng) ─────────────────────────
BANNED = [
    r"`[^`]+`",                                   # tên bảng / cột đặt trong dấu `
    r"\b[a-z]+_[a-z0-9_]+\b",                     # snake_case: tên bảng, cột, tham số
    r"\b(sale|finance|accounting|human)\.[a-z_]", # mã quyền dạng sale.xxx
    r"\b[A-Z][a-z]+[A-Z][A-Za-z]+\b",             # CamelCase: tên class / component
    r"\.(php|vue|js|py|blade)\b",                 # tên file
    r"\b(BE|FE|API|HTTP|JSON|SQL)\b",
    r"\b(400|401|403|404|422|423|500)\b",         # mã lỗi kỹ thuật
    r"is_can_|form_version|status\s*=",
    r"/api/|localStorage|number_format|per_page",
    r"/finance/|\?type=",                         # đường dẫn kỹ thuật — chỉ được ở cột Đường dẫn chương 9
]


def check_terms(path, path_tables):
    d = Document(path)
    texts = [p.text for p in d.paragraphs]
    allowed_idx = set()
    for i, t in enumerate(d.tables):
        # bảng chương 9 là bảng có tiêu đề cột thứ 2 = "Đường dẫn"
        if len(t.columns) >= 2 and t.cell(0, 1).text == "Đường dẫn":
            allowed_idx.add(i)
    for i, t in enumerate(d.tables):
        for r_i, row in enumerate(t.rows):
            for c_i, cell in enumerate(row.cells):
                if i in allowed_idx and c_i == 1:
                    continue
                texts.append(cell.text)
    blob = "\n".join(texts)
    found = {}
    for pat in BANNED:
        hits = re.findall(pat, blob)
        if hits:
            found[pat] = sorted(set(h if isinstance(h, str) else "".join(h) for h in hits))[:5]
    emo = re.findall(u"[☀-➿️\U0001F300-\U0001FAFF]", blob)
    if emo:
        found["emoji"] = sorted(set(emo))
    if found:
        print("!!! CON THUAT NGU KY THUAT:", found)
    else:
        print("OK - sach thuat ngu code")
    return not found


if __name__ == "__main__":
    ok = True
    for k in ("sale", "market"):
        out, pts = build(k)
        d = Document(out)
        h1 = [p.text for p in d.paragraphs if p.style.name == "Heading 1"]
        print("==", os.path.basename(out))
        print("Heading 1: %d | Heading 2: %d | Bang: %d | Doan: %d" % (
            len(h1), sum(1 for p in d.paragraphs if p.style.name == "Heading 2"), len(d.tables), len(d.paragraphs)))
        for t in h1:
            print("   ", t)
        ok &= len(h1) == 12
        ok &= check_terms(out, pts)
    sys.exit(0 if ok else 1)
