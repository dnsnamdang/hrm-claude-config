# -*- coding: utf-8 -*-
"""Sinh 2 tai lieu MO TA NGHIEP VU (skill business-flow-documenter):
  - Phieu giao chi tieu kinh doanh theo phong ban (#11643)
  - Phieu giao chi tieu kinh doanh theo nhan vien (#11651)
Nguon: code worktree develop (hrm-api Modules/Finance BusinessTarget*, hrm-client business-target-*),
menu HRM sale-hub.js, menu ERP topmenubar.blade.php, design.md + spec + plan.md cung thu muc.
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
NGAY = "20/11/2026"


# ───────────────────────── Khung dùng chung ─────────────────────────
class Doc:
    """Bọc python-docx + gom toàn bộ chữ để chạy bộ kiểm thuật ngữ."""

    def __init__(self, ten_man, phan_he):
        self.d = Document()
        st = self.d.styles["Normal"]
        st.font.name = "Times New Roman"
        st.font.size = Pt(12)
        self.texts = []          # chữ phải sạch thuật ngữ code
        self.route_texts = []    # cột "Đường dẫn" chương 9 (skill cho phép)
        self.headings = []
        self._cover(ten_man, phan_he)

    def _cover(self, ten_man, phan_he):
        for text, size in (("MÔ TẢ NGHIỆP VỤ", 20), (ten_man, 16)):
            p = self.d.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.bold = True
            r.font.size = Pt(size)
        p = self.d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("%s · Cập nhật ngày %s" % (phan_he, NGAY))
        self.texts += [ten_man, phan_he]
        self.d.add_page_break()

    def h(self, text, level):
        self.d.add_paragraph(text, style="Heading %d" % level)
        self.texts.append(text)
        if level == 1:
            self.headings.append(text)

    def para(self, text, bold_prefix=None):
        p = self.d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            p.add_run(bold_prefix).bold = True
            self.texts.append(bold_prefix)
        p.add_run(text)
        self.texts.append(text)

    def bullet(self, text, bold_prefix=None):
        p = self.d.add_paragraph(style="List Bullet")
        if bold_prefix:
            p.add_run(bold_prefix).bold = True
            self.texts.append(bold_prefix)
        p.add_run(text)
        self.texts.append(text)

    def table(self, rows, route_col=None):
        t = self.d.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = "Light Grid Accent 1"
        t.alignment = 1
        for i, row in enumerate(rows):
            assert len(row) == len(rows[0]), row
            for j, val in enumerate(row):
                t.cell(i, j).text = val
                if route_col is not None and j == route_col and i > 0:
                    self.route_texts.append(val)
                else:
                    self.texts.append(val)
        return t

    def save(self, path):
        self.d.save(path)


# Bộ kiểm thuật ngữ — BANNED copy từ testcase-documenter/assets/tc_engine.py + mẫu riêng của tài liệu nghiệp vụ.
BANNED = [
    r"`[a-z_]{3,}`",
    r"\bBE\b", r"\bFE\b",
    r"\bHTTP\b", r"\b(4\d{2}|5\d{2}) Forbidden\b",
    r"trả (400|403|404|422)", r"\b(400|403|404|409|422|423)\b",
    r"permission id", r"\bAPI /", r"/api/v1", r"localStorage",
    r"number_format", r"meta\.", r"sort_by", r"per_page",
    r"role_has_permissions", r"current_company_role",
    # thêm cho mô tả nghiệp vụ
    r"\b[a-z]+_[a-z0-9_]+\b",                  # tên bảng / cột / mã kỹ thuật dạng snake_case
    r"\bsale\.[a-z]",                            # mã quyền
    r"\.(php|vue|js|blade|py)\b",                # tên file
    r"\b[A-Z][a-z]+[A-Z][A-Za-z]+\b",            # tên class / component CamelCase
    r"\bAPI\b", r"\bJSON\b", r"\bendpoint\b", r"\bcontroller\b", r"\bservice\b",
    r"\bmiddleware\b", r"\bquery\b", r"\btransaction\b",
    r"/finance", r"\?type=",                      # đường dẫn chỉ được nằm ở cột Đường dẫn chương 9
]
# Biểu tượng cảm xúc (không tính mũi tên → dùng cho đường bấm menu).
EMOJI = u"[☀-➿\U0001F300-\U0001FAFF]"


def check_terms(doc, label):
    blob = "\n".join(doc.texts)
    found = {}
    for pat in BANNED:
        hits = re.findall(pat, blob)
        if hits:
            found[pat] = len(hits)
    emo = re.findall(EMOJI, blob)
    if emo:
        found["emoji"] = sorted(set(emo))
    if found:
        print("!!! [%s] CON THUAT NGU KY THUAT:" % label, found)
    else:
        print("OK [%s] - khong con thuat ngu ky thuat / emoji (cot Duong dan chuong 9 duoc mien)" % label)
    # cột Đường dẫn: chỉ được là route màn
    for r in doc.route_texts:
        if not re.fullmatch(r"(/finance/business-target-(departments|employees)(/<số>)?(\?type=for-approve)?|…\?type=for-approve)", r):
            print("!!! [%s] Cot Duong dan la:" % label, r)
    return found


# ───────────────────────── Đoạn dùng chung 2 phiếu ─────────────────────────
NHOM_SO = ("Mỗi dòng có 8 ô nhập: Khách hãng / Khách khác × Hàng hóa / Dịch vụ × SL khách / Doanh số. "
           "Bảng hiện thêm 4 cột Tổng cộng (= Khách hãng + Khách khác) chỉ để xem, không nhập.")


def chuong_7_pham_vi(doc, ten_duyet):
    doc.table([
        ["Quyền người dùng đang có", "Nhìn thấy những phiếu nào trên danh sách"],
        ["“Xem chỉ tiêu” ở mức Tổng công ty", "Phiếu của mọi công ty."],
        ["“Xem chỉ tiêu” ở mức Công ty", "Phiếu của công ty đang làm việc."],
        ["Không có quyền “Xem chỉ tiêu”", "Chỉ phiếu do chính mình lập."],
        ["Cộng thêm, nếu có “%s”" % ten_duyet, "Phiếu đang Chờ duyệt của công ty đang làm việc."],
        ["Cộng thêm, với mọi người", "Phiếu do chính mình đã duyệt."],
        ["Không có quyền nào", "Vẫn vào được màn hình (mục menu chính không bị ẩn) nhưng danh sách chỉ có phiếu do "
         "mình lập — thường là trống. Không có nút “Tạo mới”. Mở phiếu của người khác bằng đường dẫn thì hệ "
         "thống báo phiếu không tồn tại hoặc không có quyền xem và đưa về danh sách."],
    ])
    doc.para("Hai quy tắc áp cho mọi trường hợp trên:")
    doc.bullet("Phiếu “Đang tạo” chỉ người lập nhìn thấy — kể cả người có quyền xem mức Tổng công ty cũng không thấy phiếu "
               "nháp của người khác.")
    doc.bullet("Quyền “Xem chỉ tiêu” dùng chung cho cả hai loại phiếu giao chỉ tiêu (theo phòng ban và theo nhân viên). "
               "Quyền tính theo công ty đang làm việc; tài khoản quản trị cấp cao không có đặc quyền riêng, cũng phải "
               "được cấp quyền như mọi người.")


def chuong_6_quy_uoc(doc, ky_hieu, khong_gui_extra):
    doc.h("Quy ước chung", 2)
    doc.bullet("Thông báo hiện ở chuông thông báo trên thanh công cụ, đồng thời đẩy về ứng dụng điện thoại và hiện hộp "
               "thông báo nổi nếu người nhận đang mở hệ thống.")
    doc.bullet("Khuôn chữ: “[%s] <Hành động>: <Số phiếu>”, số phiếu in đậm; riêng Từ chối có thêm “. Lý do: <lý do>”. "
               "Cả câu tối đa 180 ký tự; lý do dài bị cắt bớt, người nhận bấm “Xem thêm” để đọc đủ." % ky_hieu)
    doc.bullet("Hệ thống không loại trừ người thao tác: người gửi duyệt nếu chính mình cũng có quyền Duyệt vẫn nhận thông "
               "báo Gửi duyệt; người lập tự duyệt phiếu của mình vẫn nhận thông báo Đã duyệt.")
    doc.bullet("Gửi thông báo lỗi (ví dụ mất kết nối máy chủ thông báo) KHÔNG làm hỏng thao tác: phiếu vẫn đổi trạng thái "
               "bình thường, lỗi chỉ được ghi lại để quản trị kiểm tra.")
    doc.bullet("Những sự kiện KHÔNG phát sinh thông báo: Lưu (nháp), Sửa, Hủy phiếu, In, Xuất Excel, xem Lịch sử, và mọi "
               "thao tác bị hệ thống chặn (gửi khi chưa có doanh số, chưa có người duyệt, trạng thái đã thay đổi…). "
               + khong_gui_extra)


def chuong_9_luu_y(doc):
    doc.para("Ba điều người đọc hay hiểu nhầm:")
    doc.bullet("Đường dẫn quyết định PHẠM VI xem, không phải quyền: người không có quyền Duyệt mà mở đường dẫn “chờ duyệt” "
               "thì danh sách trống; người không có quyền Xem chỉ tiêu mở đường dẫn chính thì vẫn chỉ thấy phiếu của mình.")
    doc.bullet("Nút “Làm mới” chỉ xoá điều kiện lọc, không đưa người dùng sang phạm vi khác — đang ở danh sách chờ duyệt "
               "thì vẫn ở danh sách chờ duyệt.")
    doc.bullet("Đường dẫn kèm giá trị lạ thì hệ thống bỏ qua, giữ phạm vi mặc định của lối vào chính.")


def chuong_10_chung(doc, cot3, loc_them, muc_khoa):
    doc.h("10.1. Tra cứu trên danh sách", 2)
    doc.bullet("Tìm nhanh: tìm theo số phiếu (gõ một phần số phiếu cũng được).")
    doc.bullet("Tìm kiếm nâng cao: %sNăm · Người tạo · Người duyệt · Trạng thái. Ô Công ty chỉ hiện với người có quyền "
               "xem mức Tổng công ty. Ở lối vào “chờ duyệt” không có ô Trạng thái (danh sách đã cố định là Chờ duyệt). "
               "%s đã ngừng hoạt động mà còn phiếu thì vẫn có trong ô lọc, đánh dấu biểu tượng khoá." % (loc_them, muc_khoa))
    doc.bullet("Cột: STT · Số phiếu (bấm để mở màn Chi tiết) · %s · Năm · Người tạo · Ngày tạo · Người duyệt · Ngày duyệt "
               "(ẩn sẵn, bật được) · Trạng thái · Hành động. Bấm tiêu đề cột để sắp xếp; mặc định phiếu tạo mới nhất "
               "lên đầu; 10 dòng mỗi trang; nút “Cấu hình cột hiển thị” để bật/tắt cột." % cot3)
    doc.bullet("Điều kiện lọc được nhớ lại trong 10 phút khi rời màn rồi quay lại.")
    doc.h("10.2. In và xuất", 2)


# ═════════════════════════ PHIẾU THEO PHÒNG BAN (#11643) ═════════════════════════
def build_phong_ban():
    ten = "Phiếu giao chỉ tiêu kinh doanh theo phòng ban"
    doc = Doc(ten, "Phân hệ Bán hàng → Kế hoạch → Giao chỉ tiêu kinh doanh · Redmine #11643")
    duyet_pb = "Duyệt chỉ tiêu kinh doanh theo phòng ban"
    tao_pb = "Tạo chỉ tiêu kinh doanh theo phòng ban"

    # 1
    doc.h("1. TÀI LIỆU NÀY DÀNH CHO AI", 1)
    doc.para("Tài liệu mô tả nghiệp vụ của chức năng “Phiếu giao chỉ tiêu kinh doanh theo phòng ban” sau khi chuyển từ "
             "phần mềm ERP sang hệ thống HRM: chức năng dùng để làm gì, ai tham gia, phiếu đi qua những bước nào, mỗi "
             "bước ai nhận thông báo, và những quy tắc bắt buộc. Tài liệu không hướng dẫn bấm từng nút (xem tài liệu "
             "Hướng dẫn sử dụng) và không đặc tả từng trường (xem tài liệu SRS).")
    doc.bullet("Người lập chỉ tiêu cho công ty và người duyệt: hiểu mình làm gì ở từng bước.")
    doc.bullet("Trưởng phòng kinh doanh: hiểu chỉ tiêu của phòng mình đến từ đâu và khi nào dùng được để chia cho nhân viên.")
    doc.bullet("Cán bộ quản lý, người nghiệm thu: đối chiếu hệ thống có chạy đúng nghiệp vụ không.")
    doc.bullet("Bộ phận kiểm thử: dùng kèm file test case cùng thư mục tài liệu.")

    # 2
    doc.h("2. CHỨC NĂNG NÀY DÙNG ĐỂ LÀM GÌ", 1)
    doc.h("2.1. Mục đích", 2)
    doc.para("Đầu mỗi năm, công ty giao chỉ tiêu kinh doanh cho các phòng ban: mỗi phòng, tại mỗi Tỉnh/TP phụ trách, phải "
             "đạt bao nhiêu khách hàng và bao nhiêu doanh số, tách theo Hàng hóa / Dịch vụ và theo Khách hãng / Khách "
             "khác. Phiếu giao chỉ tiêu theo phòng ban ghi nhận chính thức con số đó, đi qua bước duyệt, và sau khi được "
             "duyệt thì trở thành con số chuẩn mà các phần khác của hệ thống dùng chung.")
    doc.para("Phiếu được tổ chức theo cây: Khối kinh doanh → Khu vực → Tỉnh/TP → Phòng ban → (tuỳ chọn) Bộ phận. "
             "Mỗi phiếu dành cho một công ty trong một năm. " + NHOM_SO)
    doc.h("2.2. Vị trí trong luồng lớn", 2)
    doc.para("Đây là bước ĐẦU của quy trình giao chỉ tiêu hai bước:")
    doc.bullet("Bước 1 — Phiếu giao chỉ tiêu theo phòng ban (tài liệu này): công ty giao cho phòng, theo Tỉnh/TP.")
    doc.bullet("Bước 2 — Phiếu giao chỉ tiêu theo nhân viên: phòng chia tiếp chỉ tiêu của mình cho từng nhân viên. Phiếu "
               "bước 2 tự nạp chỉ tiêu của phòng từ phiếu bước 1 ĐÃ DUYỆT cùng công ty, cùng năm. Phiếu bước 1 chưa duyệt "
               "thì phòng chưa lập được phiếu bước 2.")
    doc.bullet("Sau đó: kế hoạch bán hàng của phòng ban / công ty và báo cáo chỉ tiêu kinh doanh bên ERP đọc số của phiếu "
               "này (xem chương 11).")
    doc.h("2.3. Giá trị mang lại", 2)
    doc.bullet("Một con số chỉ tiêu duy nhất cho mỗi công ty mỗi năm, có người duyệt, không còn nhiều bản lệch nhau.")
    doc.bullet("Nhập nhanh: 8 ô số nhập thẳng trên dòng, không phải mở cửa sổ chọn từng khách hàng như bản cũ.")
    doc.bullet("Có cột “Năm trước” để so với chỉ tiêu đã duyệt của năm trước ngay khi nhập.")
    doc.bullet("Chia được chỉ tiêu của phòng xuống từng bộ phận khi cần.")
    doc.bullet("Tổng các cấp do hệ thống tự cộng, không phụ thuộc người nhập.")

    # 3
    doc.h("3. NHỮNG AI THAM GIA", 1)
    doc.table([
        ["Vai trò", "Làm gì trong nghiệp vụ này"],
        ["Người lập phiếu\n(người được cấp quyền “%s”)" % tao_pb,
         "Chọn năm, các khối kinh doanh, khu vực; nhập chỉ tiêu cho từng phòng (và bộ phận nếu chia) tại từng Tỉnh/TP; "
         "Lưu, Gửi duyệt; sửa lại khi bị Từ chối hoặc Hủy duyệt; Hủy phiếu khi không dùng nữa. Chỉ người lập mới sửa, "
         "gửi, hủy được phiếu của mình."],
        ["Người duyệt\n(người được cấp quyền “%s” tại công ty của phiếu)" % duyet_pb,
         "Nhận thông báo khi có phiếu gửi duyệt; Duyệt hoặc Từ chối (bắt buộc ghi lý do); Hủy duyệt phiếu đã duyệt khi "
         "cần sửa lại. Chỉ thao tác được với phiếu của công ty mình đang làm việc."],
        ["Cán bộ quản lý\n(người được cấp quyền “Xem chỉ tiêu”)",
         "Xem, tra cứu, in, xuất Excel phiếu trong phạm vi công ty hoặc toàn tổng công ty."],
        ["Trưởng phòng / người lập phiếu giao chỉ tiêu theo nhân viên",
         "Không thao tác trên phiếu này. Dùng chỉ tiêu Đã duyệt của phòng mình làm đầu vào cho phiếu theo nhân viên."],
        ["Các phòng ban, bộ phận kinh doanh", "Là đối tượng được giao chỉ tiêu, không thao tác trên phiếu."],
    ])

    # 4
    doc.h("4. VÒNG ĐỜI CỦA PHIẾU", 1)
    doc.para("Phiếu có 4 trạng thái, tất cả đều do chính màn hình này tạo ra; không có chứng từ nào khác cập nhật ngược "
             "trạng thái của phiếu.")
    doc.table([
        ["Trạng thái", "Ý nghĩa", "Ai làm phiếu chuyển sang trạng thái này"],
        ["Đang tạo (nhãn xám)", "Phiếu nháp, sửa được. Chỉ người lập nhìn thấy.",
         "Người lập bấm “Lưu”; hoặc người duyệt bấm “Từ chối” (phiếu Chờ duyệt quay về) hoặc “Hủy duyệt” (phiếu Đã duyệt "
         "quay về)."],
        ["Chờ duyệt (nhãn cam)", "Đã gửi, đang chờ người duyệt. Không sửa được.",
         "Người lập bấm “Lưu và gửi” ở màn Tạo/Sửa, hoặc “Gửi duyệt” ở danh sách / màn Chi tiết."],
        ["Đã duyệt (nhãn xanh lá)", "Chỉ tiêu chính thức của công ty cho năm đó; là đầu vào của phiếu theo nhân viên.",
         "Người duyệt bấm “Duyệt”."],
        ["Hủy (nhãn đỏ)", "Phiếu bỏ đi, không sửa, không in, không xuất được nữa; công ty được lập phiếu khác cho năm đó.",
         "Người lập bấm “Hủy phiếu” khi phiếu đang Đang tạo hoặc Chờ duyệt."],
    ])
    doc.para("Không có trạng thái “Từ chối” riêng: phiếu bị từ chối quay về Đang tạo và hiện dòng “Lý do từ chối: …” ở đầu "
             "phiếu cho tới khi người lập gửi lại. Phiếu không xoá được — thay bằng Hủy phiếu để giữ dấu vết. Phiếu Đã duyệt "
             "muốn hủy thì phải Hủy duyệt trước.")

    # 5
    doc.h("5. LUỒNG HOẠT ĐỘNG CHI TIẾT", 1)
    doc.h("5.1. Bước 0 — Danh mục cần có trước", 2)
    doc.bullet("Khối kinh doanh của công ty (đang hoạt động) — mỗi khối thành một tab trên phiếu.")
    doc.bullet("Khu vực và Tỉnh/TP thuộc từng khu vực — chọn khu vực là thêm các Tỉnh/TP của khu vực đó.")
    doc.bullet("Phòng ban đã được gán vào khối kinh doanh — chỉ phòng thuộc khối mới chọn được trong tab của khối đó.")
    doc.bullet("Bộ phận của phòng (nếu muốn chia chỉ tiêu xuống bộ phận).")
    doc.bullet("Ít nhất một người được cấp quyền “%s” tại công ty — thiếu thì phiếu không gửi duyệt được." % duyet_pb)

    doc.h("5.2. Bước 1 — Lập phiếu", 2)
    doc.para("Người lập bấm “Tạo mới” trên danh sách. Phiếu luôn thuộc công ty của người lập (không có ô chọn công ty). "
             "Đầu phiếu có:")
    doc.bullet("Năm (bắt buộc), mặc định năm hiện tại.")
    doc.bullet("Khối kinh doanh (bắt buộc, chọn nhiều). Mỗi khối chọn thêm một tab; luôn có thêm tab “Tổng hợp”.")
    doc.para("Trong tab của từng khối:")
    doc.bullet("Chọn Khu vực (bắt buộc, chọn nhiều) → hệ thống thêm các Tỉnh/TP của khu vực, mỗi tỉnh sẵn một dòng phòng trống.")
    doc.bullet("Mỗi Tỉnh/TP hiện theo thứ tự: dòng tỉnh (số La Mã, tên tỉnh kèm số phòng, các ô là tổng) → dòng “Năm trước” "
               "(chỉ đọc) → các dòng phòng → dưới mỗi phòng là các dòng bộ phận nếu đã chia.")
    doc.bullet("Dòng phòng: chọn phòng (có tìm), nhập 8 ô số. Phòng đã chọn ở dòng khác trong cùng tỉnh không chọn lại được. "
               "Đường “Thêm Phòng Ban” ở dòng cuối của tỉnh.")
    doc.bullet("Đầu bảng có dòng TỔNG của khối luôn ghim trên cùng khi cuộn, kèm tóm tắt “n Tỉnh/TP · n phòng · n bộ phận”.")
    doc.bullet("Ô “Hiển thị đến cấp”: Chỉ Tỉnh/TP · Đến Phòng ban · Đến Bộ phận (mặc định, mở hết). Từng dòng tỉnh/phòng "
               "thu gọn hoặc mở rộng được bằng tay.")
    doc.bullet("“Năm trước”: số của cùng Tỉnh/TP, cùng khối trong phiếu năm trước ĐÃ DUYỆT của cùng công ty; không có thì để "
               "trống. Chỉ để tham khảo, không ràng buộc.")
    doc.para("Các thao tác trên cây và kết quả:")
    doc.table([
        ["Thao tác", "Diễn ra thế nào", "Kết quả"],
        ["Chia Bộ Phận (dòng phòng đã chọn phòng)",
         "Hệ thống nạp danh sách bộ phận của phòng; phòng chưa có bộ phận thì báo “Phòng chưa có bộ phận trong danh mục”.",
         "Số đang nhập của phòng chuyển sang dòng bộ phận đầu tiên; 8 ô của phòng thành chỉ đọc = tổng các bộ phận."],
        ["Thêm Bộ Phận", "Thêm một dòng bộ phận; khoá khi đã chia hết bộ phận của phòng.",
         "Bộ phận đã chọn ở dòng khác trong cùng phòng không chọn lại được."],
        ["Xoá một bộ phận (còn nhiều bộ phận)", "Dòng có số thì hỏi “Xoá dòng <bộ phận> của <phòng>? Số liệu của dòng sẽ mất.”",
         "Dòng bị bỏ, tổng phòng tính lại."],
        ["Xoá bộ phận cuối cùng", "Không hỏi.", "Phòng trở lại nhập thẳng và nhận lại đúng số của bộ phận vừa xoá."],
        ["Đổi phòng khi đã chia bộ phận", "Hỏi “Đổi phòng? Các bộ phận đã chia sẽ bị bỏ.”",
         "Đồng ý: bỏ các dòng bộ phận, phòng mới giữ số tổng cũ để nhập thẳng."],
        ["Xoá dòng phòng", "Dòng có số thì hỏi “Xoá dòng <phòng> tại <tỉnh>? Số liệu của dòng sẽ mất.”",
         "Dòng bị bỏ. Riêng dòng phòng cuối cùng của tỉnh chỉ được làm trống, không xoá hẳn."],
        ["Bỏ một khu vực", "Nếu có tỉnh của khu vực đã nhập số thì hỏi “Bỏ vùng <tên>? <n> Tỉnh/TP có số liệu sẽ bị xoá.”",
         "Các Tỉnh/TP của khu vực bị bỏ khỏi khối."],
        ["Bỏ một khối kinh doanh", "Nếu khối đã có số thì hỏi “Bỏ khối <tên>? Số liệu đã nhập của khối sẽ mất.”",
         "Tab của khối biến mất cùng toàn bộ số đã nhập."],
        ["Đổi năm", "Không hỏi.", "Cột “Năm trước” của mọi khối nạp lại theo năm mới."],
    ])
    doc.para("Tab “Tổng hợp” (chỉ đọc): dòng TỔNG CỘNG ở đầu, sau đó mỗi Tỉnh/TP (gộp mọi khối) gồm dòng tổng của tỉnh, "
             "dòng Năm trước và một dòng cho từng khối có tỉnh đó.")

    doc.h("5.3. Bước 2 — Lưu hoặc Lưu và gửi", 2)
    doc.table([
        ["Hướng xử lý", "Diễn ra thế nào", "Kết quả"],
        ["Lưu", "Hệ thống kiểm các ô bắt buộc (mục 8.1), bỏ các dòng trống, tự tính lại mọi tổng và cột Năm trước, "
                "cấp số phiếu ở lần lưu đầu.",
         "Phiếu ở Đang tạo, thông báo “Đã lưu <số phiếu>”, quay về danh sách. Không gửi thông báo."],
        ["Lưu và gửi", "Như Lưu, kiểm thêm điều kiện gửi (mục 8.1). Không có hộp hỏi xác nhận.",
         "Phiếu sang Chờ duyệt, thông báo “Đã gửi duyệt <số phiếu>”, quay về danh sách; người duyệt nhận thông báo."],
        ["Gửi duyệt (phiếu đã lưu, từ danh sách hoặc màn Chi tiết)",
         "Hỏi “Gửi duyệt phiếu <số>?”; kiểm tổng doanh số > 0 và công ty đã có người duyệt.",
         "Như Lưu và gửi."],
        ["Có lỗi", "Ô lỗi viền đỏ kèm câu lỗi; tab có lỗi có chấm đỏ; hệ thống chuyển sang tab lỗi đầu tiên, mở nhánh "
                   "đang thu gọn và cuộn tới ô lỗi; hiện “Vui lòng kiểm tra lại dữ liệu nhập”.",
         "Không lưu gì. Lỗi về trạng thái / điều kiện gửi hiện bằng thông báo nổi."],
        ["Rời màn khi chưa lưu", "Hệ thống hỏi trước khi rời.", "Chọn ở lại để lưu, hoặc rời và bỏ thay đổi."],
    ])

    doc.h("5.4. Bước 3 — Duyệt", 2)
    doc.para("Người duyệt mở phiếu từ thông báo, từ danh sách “chờ duyệt” hoặc bấm “Duyệt” ở dòng trên danh sách (nút này "
             "chỉ mở màn Chi tiết để xem kỹ trước khi quyết định). Tại màn Chi tiết:")
    doc.table([
        ["Hướng xử lý", "Diễn ra thế nào", "Kết quả"],
        ["Duyệt", "Hỏi “Duyệt phiếu <số>? Phiếu đã duyệt không sửa được.”",
         "Phiếu Đã duyệt, ghi người duyệt và ngày duyệt; người lập nhận thông báo; quay về danh sách."],
        ["Từ chối", "Hỏi “Từ chối phiếu <số>? Phiếu trở về Đang tạo để người lập sửa.” kèm ô Lý do bắt buộc.",
         "Phiếu về Đang tạo, lý do hiện ở đầu phiếu; người lập nhận thông báo kèm lý do; quay về danh sách."],
    ])

    doc.h("5.5. Bước 4 — Sửa lại sau khi bị từ chối", 2)
    doc.para("Người lập mở phiếu (dòng “Lý do từ chối” hiện ở đầu), bấm Sửa, chỉnh rồi Lưu và gửi lại. Khi gửi lại, lý do từ "
             "chối cũ được xoá.")

    doc.h("5.6. Bước 5 — Hủy duyệt phiếu đã duyệt", 2)
    doc.para("Là đường duy nhất để sửa phiếu đã duyệt (không có “Thu hồi”). Người có quyền Duyệt của công ty bấm “Hủy duyệt”:")
    doc.table([
        ["Tình huống", "Diễn ra thế nào", "Kết quả"],
        ["Chưa có phiếu theo nhân viên nào dùng chỉ tiêu",
         "Hỏi “Hủy duyệt phiếu <số>? Phiếu trở về Đang tạo để người lập sửa.”",
         "Phiếu về Đang tạo, xoá người duyệt / ngày duyệt; người lập nhận thông báo; quay về danh sách."],
        ["Đã có phiếu theo nhân viên Chờ duyệt hoặc Đã duyệt cùng công ty, cùng năm, của một phòng có trong phiếu này",
         "Hệ thống chặn, báo “Đã có phiếu giao chỉ tiêu theo nhân viên <số> dùng chỉ tiêu của phiếu này, cần hủy duyệt/từ "
         "chối phiếu đó trước”.",
         "Phiếu giữ Đã duyệt. Phải xử lý các phiếu theo nhân viên đó trước."],
        ["Phiếu theo nhân viên liên quan còn Đang tạo", "Không chặn.",
         "Lần mở Sửa sau, phiếu theo nhân viên tự nạp chỉ tiêu mới nhất của phòng."],
    ])

    doc.h("5.7. Bước 6 — Hủy phiếu", 2)
    doc.para("Người lập bấm “Hủy phiếu” khi phiếu Đang tạo hoặc Chờ duyệt. Hỏi “Hủy phiếu <số>? Phiếu Hủy không sửa được; "
             "công ty được tạo phiếu khác cho năm <năm>.” Đồng ý thì phiếu sang Hủy, không gửi thông báo.")

    # 6
    doc.h("6. THÔNG BÁO — AI NHẬN, KHI NÀO, NỘI DUNG GÌ", 1)
    doc.table([
        ["Sự kiện", "Ai nhận", "Nội dung", "Bấm vào thì đi đâu"],
        ["Gửi duyệt (Lưu và gửi / Gửi duyệt)",
         "TẤT CẢ nhân viên được cấp quyền “%s” tại công ty của phiếu (theo vai trò của công ty đó) — không phải chỉ một "
         "người, không theo phòng ban." % duyet_pb,
         "[CTKD] Gửi duyệt: <Số phiếu>", "Màn Chi tiết đúng phiếu đó"],
        ["Duyệt", "Chỉ người lập phiếu (một người)", "[CTKD] Đã duyệt: <Số phiếu>", "Màn Chi tiết đúng phiếu đó"],
        ["Từ chối", "Chỉ người lập phiếu", "[CTKD] Từ chối: <Số phiếu>. Lý do: <lý do người duyệt nhập>",
         "Màn Chi tiết đúng phiếu đó (có dòng Lý do từ chối)"],
        ["Hủy duyệt", "Chỉ người lập phiếu", "[CTKD] Hủy duyệt: <Số phiếu>", "Màn Chi tiết đúng phiếu đó"],
    ])
    chuong_6_quy_uoc(doc, "CTKD",
                     "Trưởng phòng / các phòng được giao chỉ tiêu KHÔNG nhận thông báo khi phiếu được duyệt — họ thấy "
                     "chỉ tiêu khi lập phiếu theo nhân viên.")

    # 7
    doc.h("7. PHÂN QUYỀN", 1)
    doc.para("Ba quyền dùng cho màn này (tên đúng như trong màn Phân quyền): “Xem chỉ tiêu” (có mức Công ty / Tổng công ty), "
             "“%s”, “%s”." % (tao_pb, duyet_pb))
    doc.h("7.1. Quyền → nhìn thấy dữ liệu nào", 2)
    chuong_7_pham_vi(doc, duyet_pb)
    doc.h("7.2. Thao tác → điều kiện được phép", 2)
    doc.table([
        ["Thao tác", "Điều kiện"],
        ["Tạo mới", "Có quyền “%s”. Nút không hiện ở lối vào “chờ duyệt”." % tao_pb],
        ["Sửa · Gửi duyệt", "Phiếu Đang tạo, do chính mình lập, và mình vẫn còn quyền “%s”." % tao_pb],
        ["Hủy phiếu", "Phiếu Đang tạo hoặc Chờ duyệt, do chính mình lập, còn quyền “%s”." % tao_pb],
        ["Duyệt · Từ chối", "Phiếu Chờ duyệt, có quyền “%s”, phiếu thuộc công ty mình đang làm việc. Ở danh sách chỉ có "
                            "“Duyệt” (mở màn Chi tiết); Từ chối thực hiện ở màn Chi tiết." % duyet_pb],
        ["Hủy duyệt", "Phiếu Đã duyệt, có quyền “%s”, cùng công ty (không bắt buộc là người đã duyệt), và chưa bị ràng buộc "
                      "bởi phiếu theo nhân viên (mục 5.6)." % duyet_pb],
        ["In · Xuất Excel 1 phiếu", "Nhìn thấy phiếu và phiếu không ở trạng thái Hủy."],
        ["Lịch sử", "Nhìn thấy phiếu."],
    ])
    doc.para("Nút không đủ điều kiện thì ẨN HẲN, không hiện dạng mờ; nút ở màn Chi tiết khớp với nút ở dòng tương ứng ngoài "
             "danh sách. Hệ thống không chặn người lập tự duyệt phiếu của chính mình nếu người đó cũng có quyền Duyệt.")

    # 8
    doc.h("8. QUY TẮC NGHIỆP VỤ BẮT BUỘC", 1)
    doc.h("8.1. Bắt buộc nhập — theo từng nút", 2)
    doc.table([
        ["Khi bấm", "Bắt buộc phải có"],
        ["Lưu", "Năm · ít nhất một Khối kinh doanh · Khu vực của từng khối · dòng phòng có số thì phải chọn phòng · dòng bộ "
                "phận có số thì phải chọn bộ phận. Lỗi hiện “Bắt buộc phải nhập”."],
        ["Lưu và gửi", "Như Lưu, thêm: mỗi khối có ít nhất một dòng đã chọn phòng · trong mỗi dòng, SL khách và Doanh số cùng "
                       "cặp phải đi đôi (“Bắt buộc nhập SL Khách vì đã có doanh số” / “Bắt buộc nhập doanh số vì đã có SL "
                       "Khách”) · tổng doanh số Hàng hóa + Dịch vụ của cả phiếu lớn hơn 0 (“Phiếu chưa có chỉ tiêu doanh số "
                       "— không gửi được”) · công ty đã có người được cấp quyền Duyệt (“Chưa phân quyền người duyệt”)."],
        ["Gửi duyệt (danh sách / màn Chi tiết)", "Tổng doanh số lớn hơn 0 và công ty đã có người duyệt (không kiểm lại "
                                                 "cặp SL khách / Doanh số — xem chương 12)."],
        ["Từ chối", "Lý do (tối đa 1.000 ký tự)."],
    ])
    doc.h("8.2. Ràng buộc dữ liệu", 2)
    doc.bullet("Một phiếu hiệu lực cho mỗi công ty mỗi năm (phiếu Hủy không tính). Trùng thì báo ngay dưới ô Năm: “Công ty "
               "đã có phiếu <số> (<trạng thái>) cho năm <năm>”. Kiểm ở cả Tạo lẫn Sửa.")
    doc.bullet("Ô số: số nguyên, không âm, tối đa 13 chữ số; hiển thị phân cách hàng nghìn bằng dấu phẩy. Ô trống được lưu là "
               "trống (khác với số 0). Ô chỉ đọc ở dòng chi tiết bằng 0 thì để trống; dòng tổng hiện 0.")
    doc.bullet("Dòng chưa chọn phòng/bộ phận và không có số bị bỏ khi lưu.")
    doc.bullet("Phòng đã chia bộ phận: số của phòng LUÔN bằng tổng các bộ phận. Số Tỉnh/TP luôn bằng tổng các phòng. Cột "
               "Năm trước do hệ thống tự lấy. Mọi số tổng được tính lại khi lưu, không tin con số trên màn hình gửi lên.")
    doc.bullet("Một phòng có thể nằm ở nhiều khối; khi phòng lập phiếu theo nhân viên, chỉ tiêu của phòng ở các khối cùng "
               "một Tỉnh/TP được cộng dồn.")
    doc.bullet("Khi lưu, toàn bộ cây trên màn hình thay thế cây cũ của phiếu.")
    doc.h("8.3. Khoá chỉnh sửa", 2)
    doc.bullet("Chỉ phiếu Đang tạo mới sửa được, và chỉ người lập sửa. Mở thẳng đường dẫn Sửa của phiếu không còn sửa được "
               "thì hệ thống chuyển về màn Chi tiết; cố lưu vẫn bị chặn với câu “Chỉ sửa được phiếu ở trạng thái Đang tạo.”")
    doc.bullet("Hai người thao tác cùng lúc (ví dụ người lập đang lưu thì người duyệt vừa duyệt): người đến sau bị chặn với "
               "câu “Trạng thái đã bị thay đổi. Vui lòng load lại trang”.")
    doc.h("8.4. Danh mục bị khoá", 2)
    doc.para("Ô chọn khối, khu vực, phòng, bộ phận chỉ liệt kê mục còn hoạt động. Phiếu cũ có phòng / bộ phận nay đã ngừng "
             "hoạt động vẫn hiện đúng tên đã lưu khi xem, in và xuất Excel.")
    doc.h("8.5. Số phiếu", 2)
    doc.para("Số phiếu tự sinh ở lần lưu đầu theo dạng <mã công ty>_CTKD_<năm>.<số thứ tự 5 chữ số>, ví dụ TPE_CTKD_2026.00012. "
             "Số thứ tự là dãy chung của mọi phiếu loại này (không đánh lại từ đầu mỗi năm). Phiếu còn Đang tạo mà đổi năm thì "
             "phần năm trong số phiếu đổi theo, số thứ tự giữ nguyên. Bị từ chối rồi gửi lại không đổi số.")

    # 9
    doc.h("9. CÁC LỐI VÀO MÀN HÌNH", 1)
    doc.para("Cùng một màn danh sách nhưng có nhiều mục menu trỏ vào, ở cả HRM lẫn ERP. Mục menu ERP mở màn HRM ở tab mới.")
    doc.table([
        ["Bấm vào đâu (phân hệ → nhóm → mục)", "Đường dẫn", "Danh sách hiện ra", "Dùng khi nào"],
        ["HRM: Bán hàng → Kế hoạch → Giao chỉ tiêu kinh doanh → Theo phòng ban",
         "/finance/business-target-departments",
         "Phiếu trong phạm vi xem của tôi (chương 7.1): phiếu mình lập, phiếu theo quyền Xem chỉ tiêu, phiếu chờ mình duyệt, "
         "phiếu mình đã duyệt",
         "Lối vào chính: lập phiếu, theo dõi, tra cứu"],
        ["HRM: Bán hàng → Phê Duyệt → Kế hoạch & chỉ tiêu → Giao chỉ tiêu chờ duyệt (chỉ hiện với người có quyền “%s”)" % duyet_pb,
         "…?type=for-approve",
         "Chỉ phiếu Chờ duyệt của công ty đang làm việc; không có nút Tạo mới, không có ô lọc Trạng thái",
         "Danh sách việc người duyệt phải làm"],
        ["ERP: Kinh doanh → Kế hoạch → Giao chỉ tiêu kinh doanh → Phiếu giao chỉ tiêu kinh doanh theo phòng ban",
         "/finance/business-target-departments", "Như lối vào chính của HRM (mở tab mới)",
         "Người dùng quen menu ERP"],
        ["ERP: Chờ duyệt → Kế hoạch - Chỉ tiêu → Giao chỉ tiêu → Phiếu giao chỉ tiêu kinh doanh theo phòng ban chờ duyệt "
         "(chỉ hiện với người có quyền Duyệt)",
         "…?type=for-approve", "Như lối vào chờ duyệt của HRM (mở tab mới)", "Người duyệt quen menu ERP"],
        ["(không có mục menu) Bấm vào thông báo ở chuông", "/finance/business-target-departments/<số>",
         "Mở thẳng màn Chi tiết của đúng phiếu được báo", "Xử lý ngay phiếu vừa được gửi / duyệt / từ chối"],
    ], route_col=1)
    chuong_9_luu_y(doc)

    # 10
    doc.h("10. TRA CỨU, IN VÀ XUẤT DỮ LIỆU", 1)
    chuong_10_chung(doc, "Công ty", "Công ty · ", "Công ty")
    doc.bullet("In 1 phiếu (danh sách hoặc màn Chi tiết): mở cửa sổ xem trước khổ A4 ngang, có đầu trang của công ty ghi trên "
               "phiếu, Số phiếu, Ngày tạo, tiêu đề “PHIẾU GIAO CHỈ TIÊU KINH DOANH THEO PHÒNG BAN”, dòng Năm · Trạng thái; "
               "mỗi khối một bảng (Năm trước · Tổng cộng · phòng · bộ phận) và mục Tổng hợp; khối ký 3 cột Người lập · "
               "Trưởng phòng · Người duyệt.")
    doc.bullet("Xuất Excel 1 phiếu: mỗi khối một trang tính (cây mở hết) cộng trang “Tổng hợp”; tên file là số phiếu.")
    doc.bullet("Xuất Excel danh sách: chọn cột cần xuất (Số phiếu, Công ty, Năm, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, "
               "Trạng thái), xuất đúng theo bộ lọc đang áp dụng, có dòng báo tiến độ khi dữ liệu nhiều.")
    doc.bullet("Phiếu Hủy không in và không xuất Excel 1 phiếu được.")
    doc.bullet("Lịch sử: mở từ hành động “Lịch sử” trên danh sách hoặc mục Lịch sử cuối màn Chi tiết; ghi Tạo mới, Thay đổi "
               "thông tin, Gửi duyệt, Duyệt, Từ chối (kèm lý do), Hủy duyệt, Hủy — ai làm, lúc nào.")

    # 11
    doc.h("11. LIÊN THÔNG VỚI HỆ THỐNG KHÁC", 1)
    doc.para("Phiếu dùng chung dữ liệu với phần mềm ERP — không có bản sao riêng. Vì vậy:")
    doc.bullet("Các phiếu cũ lập bên ERP (đều Đã duyệt) mở được ở HRM, hiện đủ 8 con số của từng dòng.")
    doc.bullet("Phiếu theo nhân viên (HRM) nạp chỉ tiêu phòng từ phiếu này khi Đã duyệt.")
    doc.bullet("Kế hoạch bán hàng của phòng ban / của công ty bên ERP đọc số của phiếu Đã duyệt.")
    doc.bullet("Báo cáo chỉ tiêu kinh doanh theo phòng ban (ERP, Kinh doanh → Báo cáo) đọc số SL khách và doanh số đã nhập "
               "trên phiếu.")
    doc.bullet("Số chia theo bộ phận chỉ dùng trong phiếu này (xem, in, xuất); mọi nơi khác vẫn đọc số tổng của phòng nên "
               "không bị cộng đôi.")
    doc.bullet("Menu lập phiếu và menu chờ duyệt bên ERP nay mở thẳng màn HRM; phiếu chỉ còn lập ở HRM.")
    doc.para("Các điểm cố ý làm khác bản ERP:")
    doc.table([
        ["Điểm khác", "ERP cũ", "HRM mới", "Lý do"],
        ["Nhập số khách", "Mở cửa sổ chọn từng khách hàng (có ô “Khách hàng mới”), hệ thống đếm số khách.",
         "Nhập thẳng 8 ô số trên dòng.", "Yêu cầu của #11643: giảm thao tác, chỉ tiêu là con số giao, không phải danh sách khách."],
        ["Cấp Bộ phận", "Không có.", "Tuỳ chọn chia phòng xuống bộ phận; phòng = tổng bộ phận.",
         "Theo bản mẫu được duyệt; nơi khác vẫn đọc tổng phòng nên số không lệch."],
        ["Sửa / xoá", "Sửa và xoá được cả phiếu đã duyệt.",
         "Chỉ sửa khi Đang tạo; không xoá, thay bằng Hủy phiếu; sửa phiếu đã duyệt phải Hủy duyệt.",
         "Giữ dấu vết, tránh đổi chỉ tiêu đã duyệt mà không ai biết."],
        ["Một phiếu mỗi kỳ", "Kiểm trùng không xét trạng thái.", "Một phiếu hiệu lực mỗi (công ty, năm), phiếu Hủy không tính.",
         "Lập lại được sau khi hủy, không bị chặn bởi phiếu đã bỏ."],
        ["Số tổng và Năm trước", "Lấy theo con số màn hình gửi lên.", "Hệ thống tự tính lại khi lưu.",
         "Tránh sai số khi màn hình tính lệch."],
        ["Hủy duyệt", "Chỉ chính người đã duyệt.",
         "Người có quyền Duyệt cùng công ty; bị chặn khi phiếu theo nhân viên đã dùng chỉ tiêu.",
         "Không phụ thuộc một người; không làm hỏng phiếu bước 2 đang chờ duyệt / đã duyệt."],
        ["Từ chối", "Có lý do.", "Bắt buộc lý do, báo người lập kèm lý do.", "Người lập biết phải sửa gì."],
        ["Thông báo khi Duyệt", "Không báo.", "Báo người lập.", "Người lập biết ngay phiếu đã có hiệu lực."],
        ["Gửi khi chưa có doanh số", "Không chặn.", "Chặn khi tổng doanh số bằng 0.", "Tránh duyệt phiếu rỗng."],
        ["Quản trị cấp cao", "Có đặc quyền riêng.", "Không có đặc quyền, phải được cấp quyền như mọi người.",
         "Quy định phân quyền chung của hệ thống mới."],
    ])

    # 12
    doc.h("12. GIỚI HẠN HIỆN TẠI", 1)
    doc.bullet("Nút “Gửi duyệt” ở danh sách và màn Chi tiết chưa kiểm cặp SL khách / Doanh số của từng dòng (chỉ “Lưu và gửi” "
               "kiểm). Tạm thời: người lập nên gửi bằng “Lưu và gửi” ở màn Sửa.")
    doc.bullet("Mở thẳng đường dẫn màn Tạo khi không có quyền Tạo thì form vẫn hiện; chỉ đến lúc bấm Lưu mới bị chặn.")
    doc.bullet("Lịch sử “Thay đổi thông tin” chỉ ghi số phiếu và năm, chưa ghi giá trị cũ → mới của từng ô số.")
    doc.bullet("Ô số gõ có dấu chấm (ví dụ 2.5) thì dấu chấm bị bỏ thành 25, không báo lỗi — cần nhập số nguyên.")
    doc.bullet("Ô lọc Năm trên danh sách chỉ có từ 2023 đến năm hiện tại + 2.")
    doc.bullet("Bản in: ô Trưởng phòng chưa có tên; dưới chữ ký chưa in chức danh.")
    doc.bullet("Phiếu luôn lập cho công ty gốc trên hồ sơ của người lập (danh sách khối kinh doanh cũng theo công ty đó), "
               "trong khi quyền được tính theo công ty đang làm việc. Người đang làm việc ở công ty khác công ty gốc cần lưu ý "
               "trước khi lập phiếu.")
    doc.bullet("Không có “Thu hồi” phiếu Chờ duyệt: muốn sửa thì nhờ người duyệt Từ chối, hoặc Hủy phiếu rồi lập lại.")
    doc.bullet("Số chia theo bộ phận mới chỉ để lưu, xem, in, xuất; phiếu theo nhân viên, kế hoạch và báo cáo vẫn dùng tổng phòng.")
    doc.bullet("Danh sách khách hàng chi tiết của các phiếu cũ bên ERP không hiển thị ở HRM (HRM chỉ hiện 8 con số).")
    doc.bullet("Mục “Phát triển sản phẩm” cùng nhóm menu Giao chỉ tiêu kinh doanh chưa chuyển sang HRM.")

    out = os.path.join(HERE, "Mô tả nghiệp vụ - %s.docx" % ten)
    doc.save(out)
    return doc, out


# ═════════════════════════ PHIẾU THEO NHÂN VIÊN (#11651) ═════════════════════════
def build_nhan_vien():
    ten = "Phiếu giao chỉ tiêu kinh doanh theo nhân viên"
    doc = Doc(ten, "Phân hệ Bán hàng → Kế hoạch → Giao chỉ tiêu kinh doanh · Redmine #11651")
    duyet_nv = "Duyệt chỉ tiêu kinh doanh theo nhân viên"
    tao_nv = "Tạo chỉ tiêu kinh doanh theo nhân viên"

    # 1
    doc.h("1. TÀI LIỆU NÀY DÀNH CHO AI", 1)
    doc.para("Tài liệu mô tả nghiệp vụ của chức năng “Phiếu giao chỉ tiêu kinh doanh theo nhân viên” sau khi chuyển từ phần "
             "mềm ERP sang hệ thống HRM: chức năng dùng để làm gì, ai tham gia, phiếu đi qua những bước nào, mỗi bước ai "
             "nhận thông báo, và những quy tắc bắt buộc. Tài liệu không hướng dẫn bấm từng nút (xem Hướng dẫn sử dụng) và "
             "không đặc tả từng trường (xem SRS).")
    doc.bullet("Trưởng phòng / người quản lý phòng kinh doanh: hiểu cách chia chỉ tiêu của phòng cho từng nhân viên.")
    doc.bullet("Người duyệt: hiểu khi nào nhận phiếu và duyệt căn cứ vào đâu.")
    doc.bullet("Nhân viên kinh doanh: hiểu chỉ tiêu của mình đến từ đâu và được dùng vào đâu.")
    doc.bullet("Cán bộ quản lý, người nghiệm thu, bộ phận kiểm thử.")

    # 2
    doc.h("2. CHỨC NĂNG NÀY DÙNG ĐỂ LÀM GÌ", 1)
    doc.h("2.1. Mục đích", 2)
    doc.para("Sau khi công ty giao chỉ tiêu cho phòng (phiếu theo phòng ban đã duyệt), phòng chia tiếp chỉ tiêu đó cho từng "
             "nhân viên kinh doanh tại từng Tỉnh/TP. Phiếu giao chỉ tiêu theo nhân viên ghi nhận việc chia này, đi qua bước "
             "duyệt, và khi đã duyệt thì là chỉ tiêu chính thức của từng nhân viên. Mỗi phiếu dành cho một phòng trong một năm. "
             + NHOM_SO)
    doc.h("2.2. Vị trí trong luồng lớn", 2)
    doc.bullet("Trước: Phiếu giao chỉ tiêu theo phòng ban ĐÃ DUYỆT cùng công ty, cùng năm — nguồn của dòng “Chỉ tiêu giao” "
               "theo từng Tỉnh/TP. Chưa có phiếu đó thì phòng chưa lập được phiếu này.")
    doc.bullet("Phiếu này (bước 2): phòng chia chỉ tiêu cho nhân viên.")
    doc.bullet("Sau: Kế hoạch bán hàng của nhân viên và Kế hoạch phát triển thị trường theo nhân viên (HRM) lấy chỉ tiêu của "
               "từng nhân viên từ phiếu này khi Đã duyệt; báo cáo chỉ tiêu kinh doanh theo nhân viên bên ERP cũng đọc số "
               "của phiếu này.")
    doc.h("2.3. Giá trị mang lại", 2)
    doc.bullet("Chỉ tiêu phòng tự nạp theo từng Tỉnh/TP, không phải gõ lại.")
    doc.bullet("Thấy ngay chỗ giao vượt chỉ tiêu (ô tô màu cam) mà không bị chặn lưu.")
    doc.bullet("Chỉ tiêu gắn đúng nhân viên trong danh mục, nên kế hoạch bán hàng của từng người đọc đúng số.")

    # 3
    doc.h("3. NHỮNG AI THAM GIA", 1)
    doc.table([
        ["Vai trò", "Làm gì trong nghiệp vụ này"],
        ["Người lập phiếu\n(trưởng phòng / người quản lý phòng, có quyền “%s”)" % tao_nv,
         "Chọn năm và phòng, chia chỉ tiêu cho nhân viên tại từng Tỉnh/TP, Lưu, Gửi duyệt; sửa lại khi bị Từ chối hoặc Hủy "
         "duyệt; Hủy phiếu. Người không có quyền Xem chỉ tiêu mức Công ty trở lên chỉ lập được cho phòng mình quản lý."],
        ["Người duyệt\n(có quyền “%s” tại công ty của phiếu)" % duyet_nv,
         "Nhận thông báo, Duyệt hoặc Từ chối (bắt buộc lý do), Hủy duyệt khi cần sửa lại."],
        ["Người lập / người duyệt phiếu theo phòng ban",
         "Không thao tác trên phiếu này, nhưng phiếu của họ là đầu vào. Họ không Hủy duyệt được phiếu phòng ban khi phiếu "
         "này đang Chờ duyệt hoặc Đã duyệt."],
        ["Nhân viên kinh doanh được giao", "Không thao tác, không nhận thông báo. Dùng chỉ tiêu được giao để lập kế hoạch bán "
                                           "hàng của mình."],
        ["Cán bộ quản lý (quyền “Xem chỉ tiêu”)", "Xem, tra cứu, in, xuất Excel."],
    ])

    # 4
    doc.h("4. VÒNG ĐỜI CỦA PHIẾU", 1)
    doc.para("Phiếu có 4 trạng thái, đều do chính màn hình này tạo ra.")
    doc.table([
        ["Trạng thái", "Ý nghĩa", "Ai làm phiếu chuyển sang trạng thái này"],
        ["Đang tạo (nhãn xám)", "Phiếu nháp, sửa được. Chỉ người lập nhìn thấy. Dòng “Chỉ tiêu giao” luôn lấy số mới nhất "
                                "từ phiếu theo phòng ban.",
         "Người lập bấm “Lưu”; người duyệt bấm “Từ chối” hoặc “Hủy duyệt”."],
        ["Chờ duyệt (nhãn cam)", "Đã gửi, chờ duyệt, không sửa được. “Chỉ tiêu giao” là số chụp lại lúc lưu.",
         "Người lập bấm “Lưu và gửi” hoặc “Gửi duyệt”."],
        ["Đã duyệt (nhãn xanh lá)", "Chỉ tiêu chính thức của từng nhân viên.", "Người duyệt bấm “Duyệt”."],
        ["Hủy (nhãn đỏ)", "Phiếu bỏ đi; phòng được lập phiếu khác cho năm đó.",
         "Người lập bấm “Hủy phiếu” khi Đang tạo hoặc Chờ duyệt."],
    ])
    doc.para("Không có trạng thái Từ chối riêng (về Đang tạo, hiện “Lý do từ chối: …”). Phiếu không xoá được, chỉ Hủy.")

    # 5
    doc.h("5. LUỒNG HOẠT ĐỘNG CHI TIẾT", 1)
    doc.h("5.1. Bước 0 — Điều kiện trước", 2)
    doc.bullet("Phiếu giao chỉ tiêu theo phòng ban của công ty cho năm đó đã ĐƯỢC DUYỆT và có dòng của phòng.")
    doc.bullet("Người lập có quyền “%s” và được lập cho phòng đó (mục 7.2)." % tao_nv)
    doc.bullet("Công ty có ít nhất một người được cấp quyền “%s”." % duyet_nv)

    doc.h("5.2. Bước 1 — Chọn năm, phòng và nạp chỉ tiêu", 2)
    doc.bullet("Năm (bắt buộc), mặc định năm hiện tại.")
    doc.bullet("Phòng ban (bắt buộc, một phòng). Danh sách chỉ gồm phòng mình được lập VÀ đã có chỉ tiêu trong phiếu theo "
               "phòng ban Đã duyệt của năm đang chọn. Mặc định chọn sẵn phòng của người dùng nếu phòng đó có trong danh sách.")
    doc.bullet("Chọn xong, hệ thống nạp chỉ tiêu của phòng theo từng Tỉnh/TP (phòng nằm ở nhiều khối cùng một tỉnh thì cộng "
               "dồn), mỗi tỉnh sẵn một dòng nhân viên trống. Phòng chưa có chỉ tiêu thì báo “Phòng chưa có chỉ tiêu được "
               "duyệt cho năm <năm>”.")
    doc.bullet("Đổi Năm hoặc Phòng khi đã giao cho nhân viên thì hỏi “Đổi năm? / Đổi phòng? Dữ liệu giao nhân viên đã nhập "
               "sẽ mất.”")

    doc.h("5.3. Bước 2 — Giao chỉ tiêu cho nhân viên", 2)
    doc.para("Tab “Giao chỉ tiêu” là bảng cây Tỉnh/TP → Nhân viên:")
    doc.bullet("Đầu bảng ghim 2 dòng: TỔNG (tổng đã giao, kèm “n Tỉnh/TP · n nhân viên”) và Chỉ tiêu giao (của cả phòng).")
    doc.bullet("Mỗi Tỉnh/TP: dòng tỉnh (tổng đã giao) → dòng Chỉ tiêu giao của tỉnh → các dòng nhân viên.")
    doc.bullet("Dòng nhân viên: chọn nhân viên (tìm theo tên hoặc mã, hiển thị “Tên - Mã”, chỉ nhân viên đang làm việc của "
               "công ty); nhân viên đã giao ở dòng khác trong cùng tỉnh không có trong danh sách chọn; nhập 8 ô số; “Thêm "
               "Nhân Viên” ở dòng cuối của tỉnh.")
    doc.bullet("Xoá dòng có số thì hỏi “Xoá dòng <tên> tại <tỉnh>? Số liệu của dòng sẽ mất.”; dòng cuối cùng của tỉnh chỉ "
               "được làm trống.")
    doc.bullet("Ô “Hiển thị đến cấp”: Chỉ Tỉnh/TP · Đến Nhân viên.")
    doc.para("Giao vượt chỉ tiêu:")
    doc.table([
        ["Tình huống", "Hệ thống làm gì", "Kết quả"],
        ["Tổng đã giao (dòng TỔNG hoặc dòng tỉnh) lớn hơn Chỉ tiêu giao ở cùng cột",
         "Tô ô màu cam, rê chuột hiện “Vượt chỉ tiêu giao <phần chênh>”.", "Chỉ cảnh báo — vẫn Lưu và Gửi duyệt được."],
        ["Tổng đã giao nhỏ hơn chỉ tiêu", "Không cảnh báo.", "Vẫn Lưu và Gửi duyệt được."],
    ])
    doc.para("Tab “Tổng hợp” (chỉ đọc): STT · Nhân viên (“Tên - Mã”) · Tổng doanh số · Tỉnh/TP · Doanh số theo tỉnh; dòng đầu "
             "là tên phòng và tổng doanh số của phòng. Doanh số = Hàng hóa + Dịch vụ. Chưa giao ai thì hiện “Chưa giao chỉ "
             "tiêu cho nhân viên nào”.")

    doc.h("5.4. Bước 3 — Lưu hoặc Lưu và gửi", 2)
    doc.table([
        ["Hướng xử lý", "Diễn ra thế nào", "Kết quả"],
        ["Lưu", "Kiểm ô bắt buộc (mục 8.1); bỏ dòng trống; tự tính tổng tỉnh; chụp lại Chỉ tiêu giao của phòng tại thời điểm "
                "lưu; cấp số phiếu ở lần lưu đầu.",
         "Phiếu Đang tạo, “Đã lưu <số phiếu>”, quay về danh sách. Không gửi thông báo."],
        ["Lưu và gửi", "Như Lưu, kiểm thêm điều kiện gửi.",
         "Phiếu Chờ duyệt, “Đã gửi duyệt <số phiếu>”, quay về danh sách; người duyệt nhận thông báo."],
        ["Gửi duyệt (từ danh sách / màn Chi tiết)",
         "Hỏi “Gửi duyệt phiếu <số>?”; kiểm phòng vẫn còn chỉ tiêu đã duyệt (phiếu theo phòng ban có thể đã bị Hủy duyệt "
         "sau khi lưu nháp), tổng doanh số > 0, công ty có người duyệt.",
         "Như Lưu và gửi. Nếu phòng không còn chỉ tiêu: báo “Phòng chưa có chỉ tiêu được duyệt cho năm <năm> — mở Sửa để "
         "kiểm tra lại phiếu”."],
        ["Phòng không được phép", "Lập cho phòng ngoài danh sách được phép (ví dụ mở bằng đường dẫn khác).",
         "Chặn, báo “Bạn không được lập phiếu cho phòng ban này”."],
        ["Có lỗi ở ô", "Ô lỗi viền đỏ, chuyển tab, mở nhánh, cuộn tới ô lỗi đầu tiên.", "Không lưu gì."],
    ])

    doc.h("5.5. Bước 4 — Duyệt / Từ chối", 2)
    doc.table([
        ["Hướng xử lý", "Diễn ra thế nào", "Kết quả"],
        ["Duyệt", "Hỏi “Duyệt phiếu <số>? Phiếu đã duyệt không sửa được.”",
         "Đã duyệt, ghi người và ngày duyệt; người lập nhận thông báo; quay về danh sách. Từ đây kế hoạch bán hàng của các "
         "nhân viên đọc được chỉ tiêu."],
        ["Từ chối", "Hỏi “Từ chối phiếu <số>? Phiếu trở về Đang tạo để người lập sửa.” kèm ô Lý do bắt buộc.",
         "Về Đang tạo, người lập nhận thông báo kèm lý do; quay về danh sách."],
    ])
    doc.para("Nút “Duyệt” ở dòng trên danh sách chỉ mở màn Chi tiết; Duyệt và Từ chối thực hiện ở màn Chi tiết.")

    doc.h("5.6. Bước 5 — Sửa lại, Hủy duyệt, Hủy phiếu", 2)
    doc.bullet("Sửa lại (phiếu Đang tạo): dòng Chỉ tiêu giao nạp lại số mới nhất từ phiếu theo phòng ban; Tỉnh/TP mới phát "
               "sinh trong chỉ tiêu phòng được thêm vào.")
    doc.bullet("Hủy duyệt: người có quyền “%s” cùng công ty bấm “Hủy duyệt”, hỏi “Hủy duyệt phiếu <số>? Phiếu trở về Đang "
               "tạo để người lập sửa.” Phiếu về Đang tạo, người lập nhận thông báo. Không có ràng buộc chặn như phiếu theo "
               "phòng ban." % duyet_nv)
    doc.bullet("Hủy phiếu: người lập, khi Đang tạo hoặc Chờ duyệt; hỏi “Hủy phiếu <số>? Phiếu Hủy không sửa được; phòng được "
               "tạo phiếu khác cho năm <năm>.” Không gửi thông báo.")
    doc.bullet("Khi phiếu này đang Chờ duyệt hoặc Đã duyệt, phiếu theo phòng ban chứa phòng này không Hủy duyệt được.")

    # 6
    doc.h("6. THÔNG BÁO — AI NHẬN, KHI NÀO, NỘI DUNG GÌ", 1)
    doc.table([
        ["Sự kiện", "Ai nhận", "Nội dung", "Bấm vào thì đi đâu"],
        ["Gửi duyệt (Lưu và gửi / Gửi duyệt)",
         "TẤT CẢ nhân viên được cấp quyền “%s” tại công ty của phiếu — không theo phòng, không chỉ trưởng phòng." % duyet_nv,
         "[CTKDNV] Gửi duyệt: <Số phiếu>", "Màn Chi tiết đúng phiếu đó"],
        ["Duyệt", "Chỉ người lập phiếu", "[CTKDNV] Đã duyệt: <Số phiếu>", "Màn Chi tiết đúng phiếu đó"],
        ["Từ chối", "Chỉ người lập phiếu", "[CTKDNV] Từ chối: <Số phiếu>. Lý do: <lý do>", "Màn Chi tiết đúng phiếu đó"],
        ["Hủy duyệt", "Chỉ người lập phiếu", "[CTKDNV] Hủy duyệt: <Số phiếu>", "Màn Chi tiết đúng phiếu đó"],
    ])
    chuong_6_quy_uoc(doc, "CTKDNV",
                     "Các nhân viên được giao chỉ tiêu KHÔNG nhận thông báo, kể cả khi phiếu được duyệt.")

    # 7
    doc.h("7. PHÂN QUYỀN", 1)
    doc.para("Ba quyền dùng cho màn này: “Xem chỉ tiêu” (mức Công ty / Tổng công ty, dùng chung với phiếu theo phòng ban), "
             "“%s”, “%s”. Phiếu theo nhân viên duyệt bằng quyền “…theo nhân viên”, không dùng quyền duyệt của phiếu theo "
             "phòng ban." % (tao_nv, duyet_nv))
    doc.h("7.1. Quyền → nhìn thấy dữ liệu nào", 2)
    chuong_7_pham_vi(doc, duyet_nv)
    doc.h("7.2. Thao tác → điều kiện được phép", 2)
    doc.table([
        ["Thao tác", "Điều kiện"],
        ["Tạo mới", "Có quyền “%s”. Không hiện ở lối vào “chờ duyệt”." % tao_nv],
        ["Được chọn phòng nào", "Có “Xem chỉ tiêu” mức Công ty hoặc Tổng công ty: mọi phòng đang hoạt động của công ty. Không có: "
                                "chỉ các phòng mình được giao quản lý. Trong đó chỉ hiện phòng đã có chỉ tiêu Đã duyệt của "
                                "năm đang chọn. Hệ thống kiểm lại khi lưu."],
        ["Sửa · Gửi duyệt", "Phiếu Đang tạo, do mình lập, còn quyền “%s”." % tao_nv],
        ["Hủy phiếu", "Phiếu Đang tạo hoặc Chờ duyệt, do mình lập, còn quyền “%s”." % tao_nv],
        ["Duyệt · Từ chối", "Phiếu Chờ duyệt, có quyền “%s”, phiếu thuộc công ty mình đang làm việc." % duyet_nv],
        ["Hủy duyệt", "Phiếu Đã duyệt, có quyền “%s”, cùng công ty." % duyet_nv],
        ["In · Xuất Excel 1 phiếu", "Nhìn thấy phiếu, phiếu không ở trạng thái Hủy."],
        ["Lịch sử", "Nhìn thấy phiếu."],
    ])
    doc.para("Nút không đủ điều kiện thì ẨN HẲN; nút ở màn Chi tiết khớp với nút ở dòng ngoài danh sách. Hệ thống không chặn "
             "người lập tự duyệt phiếu của mình nếu có quyền Duyệt.")

    # 8
    doc.h("8. QUY TẮC NGHIỆP VỤ BẮT BUỘC", 1)
    doc.h("8.1. Bắt buộc nhập — theo từng nút", 2)
    doc.table([
        ["Khi bấm", "Bắt buộc phải có"],
        ["Lưu", "Năm · Phòng ban · phòng phải có chỉ tiêu Đã duyệt của năm · dòng có số thì phải chọn nhân viên · một nhân "
                "viên không xuất hiện hai lần trong cùng tỉnh (“Nhân viên đã có trong tỉnh này”)."],
        ["Lưu và gửi", "Như Lưu, thêm: cặp SL khách / Doanh số trong từng dòng phải đi đôi · tổng doanh số Hàng hóa + Dịch vụ "
                       "đã giao lớn hơn 0 (“Phiếu chưa giao chỉ tiêu doanh số cho nhân viên — không gửi được”) · công ty có "
                       "người duyệt (“Chưa phân quyền người duyệt”)."],
        ["Gửi duyệt (danh sách / màn Chi tiết)", "Phòng còn chỉ tiêu Đã duyệt · tổng doanh số > 0 · có người duyệt (không kiểm "
                                                 "lại cặp SL khách / Doanh số — xem chương 12)."],
        ["Từ chối", "Lý do (tối đa 1.000 ký tự)."],
    ])
    doc.h("8.2. Ràng buộc dữ liệu", 2)
    doc.bullet("Một phiếu hiệu lực cho mỗi (công ty, phòng, năm), phiếu Hủy không tính. Trùng thì báo dưới ô Phòng ban: "
               "“Phòng đã có phiếu <số> (<trạng thái>) cho năm <năm>”.")
    doc.bullet("Danh sách Tỉnh/TP của phiếu do chỉ tiêu phòng quyết định; người lập không thêm tỉnh ngoài chỉ tiêu.")
    doc.bullet("Dòng Chỉ tiêu giao do hệ thống tự lấy và chụp lại lúc lưu; tổng tỉnh tự cộng — không tin con số màn hình gửi lên.")
    doc.bullet("Giao vượt hay giao thiếu so với chỉ tiêu đều không bị chặn; vượt thì tô cam.")
    doc.bullet("Ô số: số nguyên không âm, tối đa 13 chữ số; ô trống lưu là trống; ô chỉ đọc bằng 0 ở dòng chi tiết để trống.")
    doc.bullet("Dòng chưa chọn nhân viên và không có số bị bỏ khi lưu.")
    doc.h("8.3. Khoá chỉnh sửa", 2)
    doc.bullet("Chỉ phiếu Đang tạo, chỉ người lập sửa. Mở thẳng đường dẫn Sửa của phiếu không sửa được thì chuyển về màn Chi "
               "tiết; cố lưu bị chặn “Chỉ sửa được phiếu ở trạng thái Đang tạo.”")
    doc.bullet("Trạng thái thay đổi giữa chừng: người đến sau bị chặn “Trạng thái đã bị thay đổi. Vui lòng load lại trang”.")
    doc.h("8.4. Danh mục bị khoá", 2)
    doc.para("Ô chọn phòng và nhân viên chỉ liệt kê phòng đang hoạt động và nhân viên đang làm việc. Phiếu cũ vẫn hiện đúng "
             "tên nhân viên, mã nhân viên, tên phòng đã lưu, kể cả khi nhân viên đã nghỉ hoặc phòng đã ngừng. Dòng “nhân viên "
             "mới” (gõ tên tự do) của phiếu ERP cũ hiện đúng tên đã gõ.")
    doc.h("8.5. Số phiếu", 2)
    doc.para("Tự sinh ở lần lưu đầu theo dạng <mã công ty>_CTKDNV_<năm>.<số thứ tự 5 chữ số>, ví dụ TPSG_CTKDNV_2026.00057. "
             "Số thứ tự là dãy chung của mọi phiếu loại này. Đổi năm khi còn Đang tạo thì phần năm đổi theo, số thứ tự giữ nguyên.")

    # 9
    doc.h("9. CÁC LỐI VÀO MÀN HÌNH", 1)
    doc.para("Cùng một màn danh sách, nhiều mục menu trỏ vào ở cả HRM lẫn ERP. Mục menu ERP mở màn HRM ở tab mới.")
    doc.table([
        ["Bấm vào đâu (phân hệ → nhóm → mục)", "Đường dẫn", "Danh sách hiện ra", "Dùng khi nào"],
        ["HRM: Bán hàng → Kế hoạch → Giao chỉ tiêu kinh doanh → Theo nhân viên",
         "/finance/business-target-employees",
         "Phiếu trong phạm vi xem của tôi (chương 7.1)", "Lối vào chính: lập phiếu, theo dõi, tra cứu"],
        ["HRM: Bán hàng → Phê Duyệt → Kế hoạch & chỉ tiêu → Giao chỉ tiêu NV chờ duyệt (chỉ hiện với người có quyền “%s”)" % duyet_nv,
         "…?type=for-approve",
         "Chỉ phiếu Chờ duyệt của công ty đang làm việc; không có nút Tạo mới, không có ô lọc Trạng thái",
         "Danh sách việc người duyệt phải làm"],
        ["ERP: Kinh doanh → Kế hoạch → Giao chỉ tiêu kinh doanh → Phiếu giao chỉ tiêu kinh doanh theo nhân viên",
         "/finance/business-target-employees", "Như lối vào chính của HRM (mở tab mới)", "Người dùng quen menu ERP"],
        ["ERP: Chờ duyệt → Kế hoạch - Chỉ tiêu → Giao chỉ tiêu → Phiếu giao chỉ tiêu kinh doanh theo nhân viên chờ duyệt "
         "(chỉ hiện với người có quyền Duyệt)",
         "…?type=for-approve", "Như lối vào chờ duyệt của HRM (mở tab mới)", "Người duyệt quen menu ERP"],
        ["(không có mục menu) Bấm vào thông báo ở chuông", "/finance/business-target-employees/<số>",
         "Mở thẳng màn Chi tiết của đúng phiếu được báo", "Xử lý ngay phiếu vừa được gửi / duyệt / từ chối"],
    ], route_col=1)
    chuong_9_luu_y(doc)

    # 10
    doc.h("10. TRA CỨU, IN VÀ XUẤT DỮ LIỆU", 1)
    chuong_10_chung(doc, "Phòng ban", "Công ty · Phòng ban (lọc theo Công ty đã chọn) · ", "Công ty / phòng ban")
    doc.bullet("In 1 phiếu: cửa sổ xem trước khổ A4 ngang, đầu trang công ty của phiếu, Số, Ngày tạo, tiêu đề “PHIẾU GIAO CHỈ "
               "TIÊU KINH DOANH THEO NHÂN VIÊN”, dòng Năm · Phòng ban · Trạng thái; bảng Giao chỉ tiêu (Chỉ tiêu giao, tổng, "
               "dòng nhân viên “Tên - Mã”) và mục Tổng hợp theo nhân viên; khối ký Người lập · Trưởng phòng · Người duyệt.")
    doc.bullet("Xuất Excel 1 phiếu: trang tính “Giao chỉ tiêu” và “Tổng hợp theo nhân viên”; tên file là số phiếu.")
    doc.bullet("Xuất Excel danh sách: chọn cột (Số phiếu, Phòng ban, Năm, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng "
               "thái), theo đúng bộ lọc, có báo tiến độ.")
    doc.bullet("Phiếu Hủy không in và không xuất Excel 1 phiếu được.")
    doc.bullet("Lịch sử: Tạo mới, Thay đổi thông tin, Gửi duyệt, Duyệt, Từ chối (kèm lý do), Hủy duyệt, Hủy.")

    # 11
    doc.h("11. LIÊN THÔNG VỚI HỆ THỐNG KHÁC", 1)
    doc.para("Phiếu dùng chung dữ liệu với phần mềm ERP:")
    doc.bullet("Các phiếu cũ lập bên ERP (đều Đã duyệt) mở được ở HRM, đủ 8 con số; dòng “nhân viên mới” cũ hiện tên đã gõ.")
    doc.bullet("Đầu vào: chỉ tiêu phòng lấy từ Phiếu giao chỉ tiêu theo phòng ban Đã duyệt (HRM).")
    doc.bullet("Đầu ra: Kế hoạch bán hàng của nhân viên và Kế hoạch phát triển thị trường theo nhân viên (HRM) lấy chỉ tiêu "
               "từng nhân viên theo Tỉnh/TP từ phiếu Đã duyệt; Báo cáo chỉ tiêu kinh doanh theo nhân viên (ERP) đọc số đã nhập.")
    doc.bullet("Menu lập phiếu và menu chờ duyệt bên ERP nay mở thẳng màn HRM; phiếu chỉ còn lập ở HRM.")
    doc.para("Các điểm cố ý làm khác bản ERP:")
    doc.table([
        ["Điểm khác", "ERP cũ", "HRM mới", "Lý do"],
        ["Nhập số khách", "Mở cửa sổ chọn từng khách hàng.", "Nhập thẳng 8 ô số.", "Yêu cầu #11651, giảm thao tác."],
        ["Nhân viên mới", "Gõ tên tự do người chưa có trong danh mục.",
         "Chỉ chọn nhân viên trong danh mục, không trùng trong một tỉnh.",
         "Chỉ tiêu phải gắn đúng người để kế hoạch bán hàng của nhân viên đọc được."],
        ["Giao so với chỉ tiêu", "Chặn gửi khi tổng giao chưa đủ chỉ tiêu.", "Không chặn; giao vượt thì tô cam.",
         "Theo bản mẫu được duyệt: phòng tự quyết cách chia, hệ thống chỉ cảnh báo."],
        ["Lấy chỉ tiêu phòng", "Lấy một dòng, sai khi phòng nằm ở nhiều khối cùng tỉnh.", "Cộng dồn theo Tỉnh/TP.", "Sửa lỗi số."],
        ["Quyền duyệt", "Dùng nhầm quyền duyệt của phiếu theo phòng ban.", "Dùng “%s”." % duyet_nv, "Sửa lỗi phân quyền."],
        ["Một phiếu mỗi kỳ", "Kiểm trùng theo người lập.", "Một phiếu hiệu lực mỗi (công ty, phòng, năm).",
         "Hai người không lập hai phiếu cho cùng một phòng."],
        ["Sửa / xoá", "Sửa, xoá được cả phiếu đã duyệt.", "Chỉ sửa khi Đang tạo; Hủy thay cho xoá; Hủy duyệt để sửa phiếu đã duyệt.",
         "Giữ dấu vết."],
        ["Phòng được chọn", "Quản trị cấp cao chọn mọi phòng; người khác chọn phòng mình quản lý.",
         "Người có quyền Xem chỉ tiêu mức Công ty trở lên chọn mọi phòng; người khác chọn phòng mình quản lý; chỉ phòng đã có "
         "chỉ tiêu được duyệt.", "Không còn đặc quyền quản trị; tránh lập phiếu cho phòng chưa có chỉ tiêu."],
        ["Số tổng và chỉ tiêu", "Lấy theo con số màn hình gửi lên.", "Hệ thống tự tính / tự lấy khi lưu.", "Tránh sai số."],
        ["Thông báo khi Duyệt", "Không báo.", "Báo người lập.", "Người lập biết phiếu đã có hiệu lực."],
    ])

    # 12
    doc.h("12. GIỚI HẠN HIỆN TẠI", 1)
    doc.bullet("Nút “Gửi duyệt” ở danh sách và màn Chi tiết chưa kiểm cặp SL khách / Doanh số (chỉ “Lưu và gửi” kiểm). Tạm "
               "thời: gửi bằng “Lưu và gửi” ở màn Sửa.")
    doc.bullet("Mở thẳng đường dẫn màn Tạo khi không có quyền Tạo thì form vẫn hiện; đến lúc Lưu mới bị chặn.")
    doc.bullet("Lịch sử “Thay đổi thông tin” chỉ ghi số phiếu, năm, phòng; chưa ghi giá trị cũ → mới của từng ô số.")
    doc.bullet("Ô số gõ có dấu chấm (ví dụ 2.5) thì thành 25, không báo lỗi.")
    doc.bullet("Ô lọc Năm trên danh sách chỉ có từ 2023 đến năm hiện tại + 2.")
    doc.bullet("Bản in: ô Trưởng phòng chưa có tên; dưới chữ ký chưa in chức danh.")
    doc.bullet("Phiếu Đang tạo có Tỉnh/TP mà sau đó chỉ tiêu phòng không còn tỉnh này: mở Sửa vẫn thấy tỉnh với chỉ tiêu trống, "
               "nhưng khi lưu các dòng giao ở tỉnh đó bị bỏ đi mà không báo. Nên kiểm lại trước khi lưu.")
    doc.bullet("Hủy duyệt phiếu không bị chặn và không cảnh báo dù nhân viên đã lập kế hoạch bán hàng dựa trên chỉ tiêu này.")
    doc.bullet("Phiếu luôn lập cho công ty gốc trên hồ sơ của người lập (danh sách phòng, nhân viên cũng theo công ty đó), "
               "trong khi quyền được tính theo công ty đang làm việc. Người làm việc chéo công ty cần lưu ý.")
    doc.bullet("Không có “Thu hồi” phiếu Chờ duyệt: muốn sửa thì nhờ người duyệt Từ chối, hoặc Hủy phiếu rồi lập lại.")
    doc.bullet("Chỉ tiêu theo bộ phận ở phiếu theo phòng ban chưa được dùng: phiếu này luôn nạp tổng của phòng.")
    doc.bullet("Danh sách khách hàng chi tiết của các phiếu cũ bên ERP không hiển thị ở HRM.")

    out = os.path.join(HERE, "Mô tả nghiệp vụ - %s.docx" % ten)
    doc.save(out)
    return doc, out


def verify(path):
    d = Document(path)
    h1 = [p.text for p in d.paragraphs if p.style.name == "Heading 1"]
    print("  File:", os.path.basename(path))
    print("  Heading 1 (%d):" % len(h1), " | ".join(h1))
    print("  So bang:", len(d.tables), "| So doan:", len(d.paragraphs))
    assert len(h1) == 12, "Thieu chuong"
    for i, t in enumerate(h1, 1):
        assert t.startswith("%d. " % i), t


if __name__ == "__main__":
    for builder, label in ((build_phong_ban, "phong ban"), (build_nhan_vien, "nhan vien")):
        doc, out = builder()
        print("Da tao:", out)
        verify(out)
        check_terms(doc, label)
