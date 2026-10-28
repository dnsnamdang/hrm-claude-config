# -*- coding: utf-8 -*-
"""Phần DÙNG CHUNG để dựng HDSD bản GỌN cho các màn PHIẾU (form chuẩn = HDSD Danh mục quốc gia, TPE Pass).

Khuôn: skill hdsd-documenter (`assets/HDSD_MAU_GON.docx` + QgWriter). Mỗi màn chỉ viết 1 generator ngắn:

    from hdsd_phieu_lib import PhieuHdsd
    d = PhieuHdsd('Phiếu chuyển hàng nhập thẳng', shots_dir, icon_dirs=[...])
    d.tong_quan(thuat_ngu, phien_ban, quyen, uml_png)
    d.truy_cap(menu=[...], o_nhanh='...', bo_loc=[...])
    d.phan('LẬP PHIẾU ...'); d.step([...]); d.img('10_create', 'Màn hình ...')   # phần riêng của màn
    d.xoa(...); d.lich_su(...); d.xuat_excel(); d.cai_dat_bo_loc(); d.tuy_chinh_cot()
    d.save(out_docx)            # dựng lại mục lục + lưu
    finalize_word(out_docx)     # Word (Windows COM) cập nhật mục lục, gỡ font nhúng, xuất PDF

Quy ước ảnh (thư mục shots): 01_list · 20_export · 25_colcfg · 26_filtercfg · 13_delete · 16_history …
Quy ước icon (icons/, đã chạy trim_icon.py): menu_*, o_timnhanh, o_<ô lọc>, btn_*, item_*.
Câu chữ các khối chuẩn chép theo HDSD Danh mục quốc gia đã Pass — đừng sửa tuỳ tiện.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HRM = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..', '_catalog_docs_lib'))
from qg_writer import QgWriter, strip_embedded_fonts  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402

TPL = os.path.join(HRM, '.claude', 'skills', 'hdsd-documenter', 'assets', 'HDSD_MAU_GON.docx')
ROLES = {'pagebreak': 33, 'h1': 34, 'h2': 21, 'p': 28, 'step': 43, 'sub': 49, 'sub2': 126,
         'img': 45, 'cap': 46, 'blank': 23, 'tbl2': 22, 'tbl4': 25}
NGUOI_CAP_NHAT = 'Đội phát triển phần mềm'


def h1_trang_moi(w, text):
    """Heading 1 sang trang mới bằng 'ngắt trang trước' gắn vào chính tiêu đề (không dùng đoạn ngắt
    trang riêng — trang trước vừa kín thì đoạn ngắt bị đẩy sang trang sau → dư 1 trang trắng)."""
    w.h1(text, new_page=False)
    el = w.sectPr.getprevious()
    ppr = el.find(qn('w:pPr'))
    if ppr is None:
        ppr = el.makeelement(qn('w:pPr'), {})
        el.insert(0, ppr)
    if ppr.find(qn('w:pageBreakBefore')) is None:
        pb = ppr.makeelement(qn('w:pageBreakBefore'), {})
        ps = ppr.find(qn('w:pStyle'))
        (ps.addnext(pb) if ps is not None else ppr.insert(0, pb))


def anh_lien_chu_thich(w):
    """Gắn keepNext cho đoạn ảnh vừa chèn → chú thích 'Hình N' không rơi sang trang sau."""
    cap = w.sectPr.getprevious()
    el = cap.getprevious()
    if el is None or not el.findall('.//' + qn('w:drawing')):
        return
    ppr = el.find(qn('w:pPr'))
    if ppr is None:
        ppr = el.makeelement(qn('w:pPr'), {})
        el.insert(0, ppr)
    if ppr.find(qn('w:keepNext')) is None:
        kn = ppr.makeelement(qn('w:keepNext'), {})
        ps = ppr.find(qn('w:pStyle'))
        (ps.addnext(kn) if ps is not None else ppr.insert(0, kn))


class PhieuHdsd(object):
    def __init__(self, ten, shots_dir, icon_dirs=()):
        self.ten = ten
        self.shots = shots_dir
        self.icon_dirs = list(icon_dirs) or [os.path.join(shots_dir, 'icons')]
        self.w = QgWriter(TPL, ROLES, body_from=19, cover_replace={'Danh mục khu vực': ten})
        self.n = 0
        self.vao = 'Bước 1: Truy cập vào màn hình %s.' % ten

    # ------------------------------------------------------------ viên gạch
    def ic(self, name):
        for d in self.icon_dirs:
            p = os.path.join(d, name + '.png')
            if os.path.exists(p):
                return ('img', p)
        raise AssertionError('Thiếu icon ' + name)

    def _segs(self, segs):
        """Cho phép viết icon gọn: chuỗi bắt đầu bằng '@' là tên icon."""
        if isinstance(segs, str):
            segs = [segs]
        return [self.ic(s[1:]) if isinstance(s, str) and s.startswith('@') else s for s in segs]

    def step(self, segs):
        self.w.step(self._segs(segs))

    def sub(self, segs):
        self.w.raw('sub', self._segs(segs))

    def sub2(self, segs):
        self.w.raw('sub2', self._segs(segs))

    def p(self, segs):
        self.w.p(self._segs(segs))

    def h2(self, text):
        self.w.h2(text)

    def img(self, name, cap):
        self.w.image(os.path.join(self.shots, name + '.png'), caption=cap)
        anh_lien_chu_thich(self.w)

    def phan(self, title):
        self.n += 1
        h1_trang_moi(self.w, 'PHẦN %d: %s' % (self.n, title))

    # ------------------------------------------------------------ TỔNG QUAN
    def tong_quan(self, thuat_ngu, phien_ban, quyen, uml_png):
        """phien_ban: [[số, ngày, nội dung]] (cột Người cập nhật tự điền).
        quyen: list câu, hoặc list [Chức năng, Quyền cần có]."""
        w = self.w
        h1_trang_moi(w, 'TỔNG QUAN')
        w.h2('1. Thuật ngữ sử dụng trong tài liệu')
        w.table([['Thuật ngữ', 'Giải thích']] + thuat_ngu, widths=[2.0, 4.5])
        w.h2('2. Cập nhật tài liệu')
        rows = [[v, d, NGUOI_CAP_NHAT, nd] for v, d, nd in phien_ban]
        w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung']] + rows, widths=[0.9, 1.1, 1.5, 3.0])
        w.h2('3. Quyền sử dụng')
        if quyen and isinstance(quyen[0], list):
            w.table([['Chức năng', 'Quyền cần có']] + quyen, widths=[2.0, 4.5])
        else:
            for s in quyen:
                w.p(s)
        w.h2('4. Sơ đồ chức năng tổng quan')
        w.image(uml_png, caption='Sơ đồ chức năng tổng quan màn ' + self.ten)
        anh_lien_chu_thich(w)

    # ------------------------------------------------------------ khối chuẩn
    def truy_cap(self, menu, o_nhanh, bo_loc=(), nang_cao=True, list_img='01_list'):
        """menu: [(chữ, icon)] theo thứ tự phân hệ → menu → (nhóm) → mục.
        bo_loc: [(nhãn để lọc theo, icon ô lọc)]."""
        self.phan('TRUY CẬP VÀ TÌM KIẾM')
        (m1, i1), rest = menu[0], menu[1:]
        segs = ['Bước 1: Từ phân hệ %s ' % m1, '@' + i1]
        for k, (m, i) in enumerate(rest):
            pre = ', chọn %s ' if k == len(rest) - 1 else (', tại menu %s ' if k == 0 else ', nhóm %s ')
            segs += [pre % m, '@' + i]
        self.step(segs)
        self.img(list_img, 'Màn hình ' + self.ten)
        self.step(['Bước 2: Nhập %s vào ô tìm kiếm nhanh ' % o_nhanh, '@o_timnhanh'])
        self.step(['Bước 3: Nhấn ', '@btn_timkiem'])
        k = 4
        if bo_loc:
            head = ['Bước %d: ' % k] + (['Bấm ', '@btn_timkiemnangcao', ', chọn giá trị trong '] if nang_cao
                                         else ['Chọn giá trị trong '])
            self.step(head + ['@' + bo_loc[0][1], ' để lọc theo %s' % bo_loc[0][0]])
            for lb, icon in bo_loc[1:]:
                self.sub(['Hoặc chọn giá trị ', '@' + icon, ' để lọc theo %s' % lb])
            k += 1
        self.step(['Bước %d: Chọn ' % k, '@btn_lammoi', ' để xóa giá trị đã lọc'])

    def xoa(self, cua_so, img='13_delete', doi_tuong='phiếu', them_cach=None):
        """them_cach: list segs dòng 'Hoặc …' (vd xóa từ màn chi tiết)."""
        self.phan('XÓA')
        self.step(['Bước 1: Bấm ', '@btn_xoa_row', ' ở cột Hành động'])
        if them_cach:
            self.sub(them_cach)
        self.step('Bước 2: Hệ thống hiện hộp xác nhận “%s”' % cua_so)
        self.img(img, 'Hộp xác nhận xóa ' + doi_tuong)
        self.step(['Bước 3: Bấm ', '@btn_confirm_xoa', ' để xác nhận xóa'])
        self.sub(['Hoặc bấm ', '@btn_huy_confirm', ' nếu bấm nhầm'])

    def lich_su(self, mo_chi_tiet, xem_o_chi_tiet='@btn_xemlichsu', img='16_history',
                cap='Cửa sổ Lịch sử thay đổi', icon_thang=True, bo_loc=True):
        """mo_chi_tiet: 'Số phiếu' / 'tên …' — thứ bấm để mở màn chi tiết."""
        self.phan('XEM LỊCH SỬ THAY ĐỔI')
        self.p('Cách 1: Xem lịch sử từ màn danh sách:')
        if icon_thang:
            self.step(['Ở cột Hành động, bấm ', '@btn_lichsu_row'])
            self.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_lichsu'])
        else:
            self.step(['Ở cột Hành động, bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_lichsu'])
        self.p('Cách 2: Xem lịch sử từ màn chi tiết:')
        self.step('Bước 1: Bấm vào %s để mở màn chi tiết' % mo_chi_tiet)
        self.step(['Bước 2: Ở khối Lịch sử thay đổi, chọn nút ', xem_o_chi_tiet])
        self.img(img, cap)
        k = 3
        if bo_loc:
            self.step(['Bước 3: Bấm ', '@btn_boloc_ls', ' để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày'])
            k = 4
        self.step(['Bước %d: Bấm ' % k, '@btn_dong_ls', ' để đóng cửa sổ.'])

    def xuat_excel(self, img='20_export', cua_so='Chọn trường xuất Excel'):
        self.phan('XUẤT DANH SÁCH RA EXCEL')
        self.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần lấy (xem PHẦN 1).')
        self.step(['Bước 2: Bấm nút ', '@btn_xuatexcel', '. Hệ thống mở cửa sổ “%s”.' % cua_so])
        self.img(img, 'Cửa sổ ' + cua_so)
        self.step('Bước 3: Tích chọn, kéo biểu tượng ☰ để đổi vị trí các trường cần xuất.')
        self.sub(['Hoặc bấm ', '@btn_chontatca', ' để tích tất cả các trường'])
        self.sub(['Hoặc bấm ', '@btn_bochonhet', ' để bỏ tích tất cả các trường'])
        self.step(['Bước 4: Bấm ', '@btn_xuatfile'])
        self.sub(['Hoặc bấm ', '@btn_dong_export', ' để không xuất'])
        self.step('Bước 5: Mở file Excel đã xuất.')

    def cai_dat_bo_loc(self, img='26_filtercfg'):
        self.phan('CÀI ĐẶT BỘ LỌC')
        self.step(['Bước 1: Ở khối Bộ lọc danh sách, bấm ', '@btn_caidatboloc'])
        self.img(img, 'Cửa sổ Cài đặt bộ lọc')
        self.step('Bước 2: Tích để hiện ô lọc, bỏ tích để ẩn ô lọc.')
        self.step('Bước 3: Kéo biểu tượng ⠿ ở đầu mỗi ô để đổi thứ tự.')
        self.step(['Bước 4: Bấm ', '@btn_luu', ' để áp dụng'])
        self.sub(['Hoặc bấm ', '@btn_khoiphuc', ' để trả về cấu hình ban đầu'])
        self.sub(['Hoặc bấm ', '@btn_dong_filtercfg', ' nếu muốn bỏ thay đổi.'])

    def tuy_chinh_cot(self, img='25_colcfg'):
        self.phan('TÙY CHỈNH CỘT HIỂN THỊ')
        self.step(['Bước 1: Ở màn danh sách, bấm biểu tượng ', '@btn_cauhinhcot'])
        self.img(img, 'Cửa sổ Tùy chỉnh cột')
        self.step('Bước 2: Tích để hiện cột, bỏ tích để ẩn cột.')
        self.step(['Bước 3: Bấm ', '@btn_chontatca', ' để hiện tất cả các cột.'])
        self.sub(['Hoặc bấm ', '@btn_bochonhet', ' để ẩn tất cả các cột (trừ các cột bắt buộc).'])
        self.step('Bước 4: Kéo biểu tượng ba gạch ở cuối mỗi dòng để đổi thứ tự cột.')
        self.step(['Bước 5: Bấm ', '@btn_luu_col', ' để áp dụng'])
        self.sub(['Hoặc bấm ', '@btn_dong_col', ' nếu muốn bỏ thay đổi.'])

    # ------------------------------------------------------------ lưu
    def save(self, out):
        self.w.rebuild_toc(levels=(1, 2))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        self.w.save(out)
        return out


# ---------------------------------------------------------------- Word (Windows) + kiểm
_PS_WORD = r'''
$ErrorActionPreference = 'Stop'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
  $d = $w.Documents.Open('%(docx)s', $false, $false)
  if ($d.TablesOfContents.Count -gt 0) { $d.TablesOfContents.Item(1).Update() }
  $d.Save()
  %(pdf_cmd)s
  try { $d.Close(0) } catch { }
} finally { try { $w.Quit() } catch { } }
'''


def finalize_word(docx, pdf=None):
    """Word cập nhật mục lục + lưu (PowerShell COM), gỡ font nhúng; tuỳ chọn xuất PDF để soát."""
    docx = os.path.abspath(docx)
    pdf_cmd = ''
    if pdf:
        pdf_cmd = "$d.ExportAsFixedFormat('%s', 17)" % os.path.abspath(pdf).replace("'", "''")
    ps = _PS_WORD % {'docx': docx.replace("'", "''"), 'pdf_cmd': pdf_cmd}
    subprocess.run(['powershell', '-NoProfile', '-Command', ps], check=True)
    size = strip_embedded_fonts(docx)
    return size


def toc_lines(docx):
    from docx import Document
    d = Document(docx)
    sdt = d.element.body.find(qn('w:sdt'))
    out = []
    for p in sdt.iter(qn('w:p')):
        t = ''.join(x.text or '' for x in p.iter(qn('w:t'))).strip()
        if t:
            out.append(t)
    return out


def render_check(pdf, out_dir, per_sheet=6):
    """Render mọi trang PDF ra ảnh, ghép per_sheet trang/tấm; báo trang trắng và chú thích tách ảnh."""
    import fitz
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf)
    pages, warn = [], []
    for i, pg in enumerate(doc):
        txt = pg.get_text().strip()
        imgs = [b for b in pg.get_text('dict')['blocks'] if b['type'] == 1 and (b['bbox'][3] - b['bbox'][1]) > 80]
        if not txt and not imgs:
            warn.append('Trang %d trắng' % (i + 1))
        for b in pg.get_text('dict')['blocks']:
            if b['type'] == 0:
                s = ''.join(sp['text'] for ln in b['lines'] for sp in ln['spans']).strip()
                if s.startswith('Hình ') and imgs and all(b['bbox'][1] < im['bbox'][1] for im in imgs):
                    warn.append('Trang %d: "%s" nằm trên mọi ảnh (tách khỏi ảnh?)' % (i + 1, s[:40]))
        pix = pg.get_pixmap(dpi=60)
        pages.append(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))
    sheets = []
    for s in range(0, len(pages), per_sheet):
        grp = pages[s:s + per_sheet]
        W = sum(p.width for p in grp) + 8 * len(grp)
        H = max(p.height for p in grp)
        sh = Image.new('RGB', (W, H), (120, 120, 120))
        x = 0
        for p in grp:
            sh.paste(p, (x, 0))
            x += p.width + 8
        path = os.path.join(out_dir, 'sheet_%02d.png' % (s // per_sheet + 1))
        sh.save(path)
        sheets.append(path)
    return len(pages), warn, sheets
