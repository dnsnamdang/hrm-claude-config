# -*- coding: utf-8 -*-
"""Thu vien dung chung de sinh SRS theo FORM CHUAN cua team
(file mau: .claude/skills/srs-documenter/assets/SRS_MAU.docx).

Cach dung: xem cac file .plans/gop-db/<feature>/gen_srs.py

    from srs_docx_lib import SrsDoc
    d = SrsDoc(out=..., menu=..., route=..., full_url=...)
    d.h1('1. Gioi thieu'); d.p('...'); d.bullets([...])
    d.save()

Quy uoc bat buoc (dung theo skill .claude/skills/srs-documenter/SKILL.md):
  - Trang dau: 2 dong tieu de CAN GIUA, KHONG phai Heading -> title_block()
  - Bang "Gioi thieu" 2 cot x 7-8 dong -> intro_table() (bo dong cuoi neu dacbiet=None)
  - Bang "Mo ta chi tiet giao dien" 8 cot -> ui_table();
    chuc nang CHI DOC bo cot "Bat buoc" -> ui_table(rows, required=False)
  - Bang "Danh sach event va xu ly event" 4 cot -> event_table()
  - Muc "Layout man hinh" = URL day du + ANH CHUP THAT -> layout()
  - Bieu do Use Case phai la ANH PNG that -> overview_figure() / uc_figure()

FORM MOI (user chot 2026-08-17, ban mau SRS_MAU.docx = SRS Danh muc khach hang):
  - Chi con 4 chuong: "Phan 1. Gioi thieu" / "Phan 2. Phan quyen" /
    "Phan 3. Dac ta chi tiet theo tung chuc nang" / "Phan 4. Quy tac nghiep vu"
  - DA BO: bang thong tin trang bia, muc "Pham vi", chuong "Tong quan",
    muc "Quy tac truy cap bat buoc", chuong "Danh muc chuc nang (Function list)",
    muc "Tieu chi nghiem thu", dong "Chuc nang lien quan: FR-xx"
  - Muc Layout CHI con dong "URL day du", bo dong "Menu:" va "Route (FE):"
"""
import os
import tempfile
import sys

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import srs_uml_render as uml  # noqa: E402

ACTOR_P1 = 'Người quản lý danh mục (P1)'
ACTOR_P2 = 'Người xem danh mục (P2)'
ACTOR_BOTH = 'Người dùng có quyền P1 hoặc P2'


class SrsDoc(object):
    """Mot tai lieu SRS theo form chuan."""

    def __init__(self, out, menu, route, full_url, img_dir=None, img_prefix=''):
        self.out = out
        self.menu = menu
        self.route = route
        self.full_url = full_url
        # Anh UML chi la file TRUNG GIAN — da nhung han vao .docx nen khong can giu.
        # Mac dinh ghi vao thu muc tam cua he dieu hanh de khong rai rac vao repo
        # (truoc day mac dinh la <thu muc lib>/img, gio lib nam trong skill assets).
        # Muon giu lai anh de xem thi truyen img_dir='...' khi khoi tao.
        self.img_dir = img_dir or os.path.join(tempfile.gettempdir(), 'srs_uml_img')
        self.img_prefix = img_prefix
        os.makedirs(self.img_dir, exist_ok=True)
        self._fig = 0

        doc = Document()
        sec = doc.sections[0]
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11)
        sec.left_margin = Inches(1.25)
        sec.right_margin = Inches(1.25)

        st = doc.styles['Normal']
        st.font.name = 'Calibri'
        st.font.size = Pt(11)
        for name, size in [('Heading 1', 20), ('Heading 2', 16), ('Heading 3', 14)]:
            hs = doc.styles[name]
            hs.font.size = Pt(size)
            hs.font.color.rgb = RGBColor(0x2F, 0x54, 0x96)
        self.doc = doc

    # -------------------------------------------------------- trang dau
    def title_block(self, man_hinh):
        """2 dong tieu de dau tai lieu — CAN GIUA, 24pt, KHONG dung Heading.

        Ban mau khong con dong 'Phan he: ...' va khong con bang thong tin
        (Ma man hinh / Phien ban / Ngay lap / Nguoi lap / ...).
        """
        for text in ('SOFTWARE REQUIREMENTS SPECIFICATION (SRS)',
                     'Màn hình: %s' % man_hinh):
            par = self.doc.add_paragraph()
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = par.add_run(text)
            r.bold = True
            r.font.size = Pt(24)

    # ------------------------------------------------------------- text
    def h1(self, t):
        self.doc.add_heading(t, level=1)

    def h2(self, t):
        self.doc.add_heading(t, level=2)

    def h3(self, t):
        self.doc.add_heading(t, level=3)

    def p(self, t=''):
        return self.doc.add_paragraph(t)

    def bullets(self, items):
        for it in items:
            self.doc.add_paragraph(it, style='List Bullet')

    # ------------------------------------------------------------ tables
    def table(self, headers, rows, widths=None):
        t = self.doc.add_table(rows=1, cols=len(headers))
        t.style = 'Table Grid'
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, hh in enumerate(headers):
            c = t.rows[0].cells[i]
            c.text = str(hh)
            for para in c.paragraphs:
                for r in para.runs:
                    r.bold = True
                    r.font.size = Pt(10)
        for row in rows:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                cells[i].text = '' if v is None else str(v)
                for para in cells[i].paragraphs:
                    for r in para.runs:
                        r.font.size = Pt(10)
        if widths:
            for r in t.rows:
                for i, w in enumerate(widths):
                    r.cells[i].width = Inches(w)
        self.doc.add_paragraph()
        return t

    def info_table(self, rows):
        """DEPRECATED — form moi (2026-08-17) khong con bang thong tin trang bia.

        Giu lai de cac gen_srs.py cu chay duoc; KHONG dung cho tai lieu moi.
        """
        return self.table(['Thông tin', 'Nội dung'], rows, widths=[1.8, 4.2])

    def intro_table(self, ten, mota, tacnhan, dieukien, chinh, phu, dacbiet=None):
        """Bang 'Gioi thieu' cua tung chuc nang.

        dacbiet=None  -> BO HAN dong 'Yeu cau dac biet' (bang con 7 dong).
        dacbiet=''    -> giu dong nhung de trong (ban mau van co vai cho nhu vay).
        """
        rows = [
            ('Tên chức năng', ten),
            ('Mô tả', mota),
            ('Tác nhân', tacnhan),
            ('Điều kiện ban đầu', dieukien),
            ('Dòng sự kiện chính', chinh),
            ('Dòng sự kiện phụ', phu),
        ]
        if dacbiet is not None:
            rows.append(('Yêu cầu đặc biệt', dacbiet))
        return self.table(['Mục', 'Nội dung'], rows, widths=[1.5, 4.5])

    def ui_table(self, rows, required=True, scope=True):
        """Bang 'Mo ta chi tiet giao dien' (STT tu danh).

        required=True, scope=True  -> 8 cot (mac dinh, dung cho man co nhap lieu)
        required=False             -> 7 cot, bo 'Bat buoc' (chuc nang CHI DOC:
                                      xem danh sach, xem chi tiet, lich su...)
        required=False, scope=False-> 6 cot, bo ca 'Pham vi' (hop xac nhan...)

        So o trong moi dong PHAI khop so cot da chon.
        """
        headers = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái']
        widths = [0.4, 1.2, 0.8, 0.75]
        if scope:
            headers.append('Phạm vi')
            widths.append(0.85)
        if required:
            headers.append('Bắt buộc')
            widths.append(0.6)
        headers += ['Giá trị ban đầu', 'Mô tả']
        widths += [0.85, 2.2 + (0 if scope else 0.85) + (0 if required else 0.6)]
        return self.table(
            headers,
            [(i + 1,) + tuple(r) for i, r in enumerate(rows)],
            widths=widths)

    def event_table(self, rows):
        """Bang 'Danh sach event va xu ly event' 4 cot (STT tu danh)."""
        return self.table(
            ['STT', 'Event', 'Loại event', 'Xử lý event'],
            [(i + 1,) + tuple(r) for i, r in enumerate(rows)],
            widths=[0.4, 1.6, 0.9, 3.6])

    # ------------------------------------------------- form RUT GON (2026-08-12)
    def field_table(self, rows):
        """Bang 'Mo ta chi tiet' 7 cot cua FORM RUT GON (STT tu danh).

        Cot: Field name | Placeholder | Field type | Content | Required |
             Gioi han ky tu | Ghi chu
        """
        return self.table(
            ['STT', 'Field name', 'Placeholder', 'Field type', 'Content', 'Required',
             'Giới hạn ký tự', 'Ghi chú'],
            [(i + 1,) + tuple(r) for i, r in enumerate(rows)],
            widths=[0.35, 1.15, 1.0, 0.75, 1.15, 0.6, 0.7, 1.9])

    def notice_table(self, rows):
        """Bang 'Danh sach event va thong bao' 4 cot cua FORM RUT GON (STT tu danh)."""
        return self.table(
            ['STT', 'Event', 'Loại event', 'Xử lý và thông báo'],
            [(i + 1,) + tuple(r) for i, r in enumerate(rows)],
            widths=[0.4, 1.5, 0.8, 3.8])

    def toc(self, note='Nhấn chuột phải vào mục lục → Update Field → Update entire table '
                       'để cập nhật số trang.'):
        """Chen truong Muc luc cua Word (tu sinh theo Heading 1-3)."""
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn

        par = self.doc.add_paragraph()
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), r'TOC \o "1-3" \h \z \u')
        run = OxmlElement('w:r')
        txt = OxmlElement('w:t')
        txt.text = note
        run.append(txt)
        fld.append(run)
        par._p.append(fld)
        self.doc.add_paragraph()

    # ----------------------------------------------------------- figures
    def figure(self, png_path, caption, width_in=6.0):
        self._fig += 1
        par = self.doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.add_run().add_picture(png_path, width=Inches(width_in))
        cap = self.doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cap.add_run('Hình %d: %s' % (self._fig, caption))
        r.italic = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    def _png(self, name):
        return os.path.join(self.img_dir, '%s%s.png' % (self.img_prefix, name))

    def overview_figure(self, title, actors, usecases, caption):
        """5.1 So do UML tong quan — anh PNG that."""
        png = self._png('overview')
        uml.draw_overview(png, title, actors, usecases)
        self.figure(png, caption, width_in=6.3)

    def uc_figure(self, code, name, group, relations=(), actor=ACTOR_P1, caption=None):
        """5.2.x.1 Bieu do use case cua 1 chuc nang — anh PNG that."""
        png = self._png('uc_%s' % code.lower().replace('-', ''))
        uml.draw_usecase(png, actor, code, name, group, relations)
        self.figure(png, caption or ('Biểu đồ Use Case — %s %s' % (code, name)), width_in=6.2)

    # ------------------------------------------------------------ layout
    def layout(self, note='', modal=None, route=None, shot=None, shot_caption=None,
               url=None):
        """Muc 'Layout man hinh' — URL day du + ANH CHUP THAT.

        Form moi (2026-08-17): CHI ghi dong 'URL day du'. Da BO 2 dong
        'Menu: ...' va 'Route (FE): ...' cua form cu.

        shot         : duong dan file .png chup that cua DUNG chuc nang do (6.2 inch)
        shot_caption : chu thich duoi anh; mac dinh lay theo ten chuc nang truyen vao
        route        : ghi de route rieng cho chuc nang (vd man them moi /add)
        url          : ghi de thang URL day du, uu tien hon `route`
        """
        base = url
        if base is None:
            base = self.full_url
            if route:
                base = self.full_url.replace(self.route, route) \
                    if self.route in self.full_url else self.full_url
        self.p('Đường dẫn màn hình:')
        self.bullets(['URL đầy đủ: %s' % base])
        if modal:
            self.p('Modal %s được mở ngay trên màn hình danh sách theo đường dẫn ở trên.' % modal)
        if note:
            self.p(note)
        if shot:
            if not os.path.exists(shot):
                raise IOError('Thieu anh chup cho muc Layout: %s' % shot)
            self.figure(shot, shot_caption or 'Màn hình thực tế', width_in=6.2)

    # -------------------------------------------------------------- save
    def save(self, verbose=True):
        os.makedirs(os.path.dirname(self.out), exist_ok=True)
        self.doc.save(self.out)
        if verbose:
            self.selfcheck()
        return self.out

    def selfcheck(self):
        """Buoc 4 cua skill: tu kiem tra truoc khi bao xong."""
        from docx import Document as _D
        d = _D(self.out)
        imgs = sum(1 for r in d.part.rels.values() if 'image' in r.reltype)
        bad = [x.text for x in d.paragraphs
               if any(ch in x.text for ch in ('\u250c', '\u25cb', '\u2502', '\u2514'))]
        out = ('OK %s | bang=%d | doan=%d | anh=%d | so-do-ky-tu=%d'
               % (os.path.basename(self.out), len(d.tables), len(d.paragraphs), imgs, len(bad)))
        try:
            print(out)
        except UnicodeEncodeError:
            print(out.encode('ascii', 'replace').decode())
        assert imgs > 0, 'Thieu anh bieu do use case'
        assert not bad, 'Con so do ve bang ky tu: %s' % bad[:3]
