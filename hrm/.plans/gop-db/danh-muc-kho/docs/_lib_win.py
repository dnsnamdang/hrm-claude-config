# -*- coding: utf-8 -*-
"""Bộ dựng SRS + HDSD (form "Danh mục quốc gia" — TPE duyệt) cho 7 danh mục kho, chạy trên WINDOWS.

Vì sao có file này (không sửa thư viện dùng chung):
- `_catalog_docs_lib/catalog_v2.py` trỏ ROOT/TPL/ICONS cố định vào `catalog-docs-v2/` (máy này không có `templates/`,
  `icons/`), `finalize()` gọi Word macOS, và `build_srs` KHÔNG có Phần 5 + chưa gắn "giữ ảnh liền chú thích".
- `_catalog_docs_lib/hdsd_gon.py` đọc ảnh ở `<dir>/shots`, còn danh mục kho để ảnh ở `hdsd_shots/` (đã gitignore).
=> Ở đây chỉ DÙNG LẠI `QgWriter` (qg_writer.py), bộ vai trò SRS của catalog_v2 và 2 hàm trình bày của hdsd_gon
   (`h1_trang_moi`, `anh_lien_chu_thich`); phần dựng thân bài viết lại theo dữ liệu từng màn khai trong
   `docs/<slug>/gen_srs.py`, `gen_hdsd.py`.

Thư mục một màn (`docs/<slug>/`):
  hdsd_shots/*.png        ảnh màn hình (capture.js)      hdsd_shots/icons/*.png   ảnh nút (đã trim_icon)
  uml/overview.png, uml/uc_*.png  (draw_uml)             out/*.pdf                bản xem nhanh
  SRS - <Tên màn>.docx · HDSD_<Tên màn>.docx · testcase - <Tên màn>.xlsx

Chuỗi trong dữ liệu được chèn icon bằng `{icon:ten}` (ảnh `hdsd_shots/icons/ten.png`); `**đậm**` in đậm.
"""
import os
import re
import subprocess
import sys
import zipfile

DOCS = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(DOCS, '..', '..'))
HRM_CFG = os.path.abspath(os.path.join(GOPDB, '..', '..'))          # hrm-claude-config/hrm
LIB = os.path.join(GOPDB, '_catalog_docs_lib')
SKILLS = os.path.join(HRM_CFG, '.claude', 'skills')
sys.path.insert(0, LIB)
sys.path.insert(0, os.path.join(SKILLS, 'srs-documenter', 'assets'))
sys.path.insert(0, os.path.join(SKILLS, 'testcase-documenter', 'assets'))

from qg_writer import QgWriter, strip_embedded_fonts  # noqa: E402
from catalog_v2 import SRS_ROLES, QTC_LINK  # noqa: E402
from hdsd_gon import ROLES as HDSD_ROLES, TPL as HDSD_TPL, h1_trang_moi, anh_lien_chu_thich  # noqa: E402

SRS_TPL = os.path.join(GOPDB, 'geo-catalogs-docs', 'SRS - Danh mục quốc gia.docx')
WORD_PS1 = os.path.join(GOPDB, 'phieu-theo-form-quoc-gia', 'word_finalize.ps1')
PHAN5_TITLE = 'Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu danh mục'
NGAY = '02/11/2026'

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


# ---------------------------------------------------------------------------------------------- tiện ích
class Screen(object):
    """Đường dẫn ảnh / icon của 1 màn."""

    def __init__(self, slug_dir):
        self.dir = slug_dir
        self.shots = os.path.join(slug_dir, 'hdsd_shots')
        self.icons = os.path.join(self.shots, 'icons')
        self.uml = os.path.join(slug_dir, 'uml')

    def shot(self, name):
        p = os.path.join(self.shots, name if name.endswith('.png') else name + '.png')
        assert os.path.exists(p), 'Thiếu ảnh %s' % p
        return p

    def ic(self, name, h=0.22):
        p = os.path.join(self.icons, name + '.png')
        assert os.path.exists(p), 'Thiếu icon %s' % p
        return ('img', p, h)

    def segs(self, value, h=0.22):
        """'Bấm {icon:btn_luu} để lưu' -> ['Bấm ', ('img', …), ' để lưu']"""
        if isinstance(value, (list, tuple)):
            return list(value)
        out = []
        for i, part in enumerate(re.split(r'\{icon:([a-z0-9_]+)\}', value)):
            if i % 2:
                out.append(self.ic(part, h))
            elif part:
                out.append(part)
        return out


def _table_runs_13(w):
    """Quy định 09/09/2026: mọi chữ trong bảng 13pt — ghi cỡ chữ TƯỜNG MINH cho từng run (bảng của khuôn HDSD gọn
    để trống cỡ chữ, phụ thuộc style bảng)."""
    from docx.oxml.ns import qn
    for tbl in w.doc.element.body.iter(qn('w:tbl')):
        for r in tbl.iter(qn('w:r')):
            if r.find(qn('w:t')) is None:
                continue
            rpr = r.find(qn('w:rPr'))
            if rpr is None:
                rpr = r.makeelement(qn('w:rPr'), {})
                r.insert(0, rpr)
            after = [qn('w:' + t) for t in ('highlight', 'u', 'effect', 'bdr', 'shd', 'fitText', 'vertAlign', 'rtl',
                                             'cs', 'em', 'lang', 'eastAsianLayout', 'specVanish', 'oMath')]
            for tag in ('w:sz', 'w:szCs'):
                e = rpr.find(qn(tag))
                if e is None:
                    e = rpr.makeelement(qn(tag), {})
                    nxt = next((c for c in rpr if c.tag in after), None)  # đúng thứ tự schema của rPr
                    nxt.addprevious(e) if nxt is not None else rpr.append(e)
                e.set(qn('w:val'), '26')


def _keep_with_next(w):
    """Đoạn vừa thêm (tiêu đề mục con 2.x.y) giữ cùng trang với bảng / ảnh ngay sau nó."""
    from docx.oxml.ns import qn
    el = w.sectPr.getprevious()
    ppr = el.find(qn('w:pPr'))
    if ppr is None:
        ppr = el.makeelement(qn('w:pPr'), {})
        el.insert(0, ppr)
    if ppr.find(qn('w:keepNext')) is None:
        kn = ppr.makeelement(qn('w:keepNext'), {})
        ps = ppr.find(qn('w:pStyle'))
        (ps.addnext(kn) if ps is not None else ppr.insert(0, kn))


def _fit_width(path, full=6.2):
    """Ảnh chụp cả trang (≥ 2000 px) chèn rộng 6,2"; ảnh chỉ khung popup / hộp xác nhận chèn 4,5" cho chữ vừa cỡ."""
    from PIL import Image
    return full if Image.open(path).width >= 2000 else 4.5


def _keep_next(w):
    """Đoạn ảnh vừa chèn giữ liền với chú thích (khuôn hdsd_gon.anh_lien_chu_thich)."""
    anh_lien_chu_thich(w)


def force_times_new_roman(path):
    """Khuôn quốc gia (xuất từ Google Docs) còn sót vài font khác (Arial ở dấu đoạn mục lục, Courier/Calibri ở style
    không dùng, font theme). Quy định 05/09/2026: toàn tài liệu Times New Roman -> ghi đè thẳng trong XML."""
    import shutil
    import tempfile
    tmp = tempfile.mktemp(suffix='.docx')
    pat = re.compile(rb'(w:(?:ascii|hAnsi|eastAsia|cs)=")(?!Times New Roman")[^"]*(")')
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename in ('word/document.xml', 'word/styles.xml', 'word/numbering.xml'):
                data = pat.sub(rb'\1Times New Roman\2', data)
                data = re.sub(rb' w:(?:ascii|hAnsi|eastAsia|cs)Theme="[^"]*"', b'', data)
            elif item.filename.startswith('word/theme/'):
                data = re.sub(rb'(<a:latin typeface=")[^"]*(")', rb'\1Times New Roman\2', data)
            zout.writestr(item, data)
    shutil.move(tmp, path)


def _exclude_toc_heading(w):
    """Tiêu đề "Mục lục" của khuôn SRS là Heading 2 -> Word cập nhật mục lục tự liệt kê chính nó. Đặt mức đề cương
    "văn bản thường" (giữ nguyên kiểu chữ) để mục lục không có dòng "Mục lục"."""
    # Trường TOC của khuôn là `\t "Heading 1,1,Heading 2,2,…" \u` -> phải đổi cả STYLE (kế thừa Heading 2 để giữ
    # nguyên hình thức) lẫn mức đề cương.
    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml.ns import qn
    try:
        st = w.doc.styles['TieuDeMucLuc']
    except KeyError:
        st = w.doc.styles.add_style('TieuDeMucLuc', WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = w.doc.styles['Heading 2']
    for p in w.doc.element.body.iterchildren(qn('w:p')):
        if ''.join(t.text or '' for t in p.iter(qn('w:t'))).strip() == 'Mục lục':
            ps = p.find('.//' + qn('w:pStyle'))
            if ps is not None:
                ps.set(qn('w:val'), st.style_id)
            ppr = p.find(qn('w:pPr'))
            if ppr is None:
                ppr = p.makeelement(qn('w:pPr'), {})
                p.insert(0, ppr)
            ol = ppr.makeelement(qn('w:outlineLvl'), {qn('w:val'): '9'})
            rpr = ppr.find(qn('w:rPr'))  # thứ tự schema: outlineLvl đứng trước rPr
            rpr.addprevious(ol) if rpr is not None else ppr.append(ol)
            return


def word_finalize(docx_path, pdf_path=None):
    """Word thật (PowerShell + COM, chỉ đóng đúng PID của mình): cập nhật mục lục/số trang, bỏ font nhúng, xuất PDF.
    Trả số trang."""
    args = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', WORD_PS1, '-Docx', os.path.abspath(docx_path)]
    if pdf_path:
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        args += ['-Pdf', os.path.abspath(pdf_path)]
    for attempt in (1, 2):  # lỗi RPC lúc đóng Word thì thử lại 1 lần
        r = subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if r.returncode == 0:
            break
        print('  word_finalize lỗi lần %d: %s' % (attempt, r.stderr.strip()[:300]))
    d, b = os.path.split(os.path.abspath(docx_path))
    for lock in (os.path.join(d, '~$' + b[2:]), os.path.join(d, '~$' + b)):
        if os.path.exists(lock):
            os.remove(lock)
    if r.returncode:
        raise RuntimeError(r.stderr)
    strip_embedded_fonts(docx_path)
    force_times_new_roman(docx_path)
    m = re.search(r'PAGES=(\d+)', r.stdout)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------------------------- UML
def draw_uml(scr, actor, mains, subs, rieng):
    """Sơ đồ Use Case khuôn quốc gia.
    mains: [(mã, tên, nhóm)] nối thẳng actor · subs: [(mã, tên, nhóm)] «extend» vào mains[0] (Xem danh sách)
    rieng: [(mã, tên, nhóm, file)] — sơ đồ riêng (actor -> 1 use case) chỉ cho chức năng thao tác + Xem chi tiết."""
    import srs_uml_render as U
    from PIL import Image, ImageDraw
    os.makedirs(scr.uml, exist_ok=True)
    U.draw_overview2(os.path.join(scr.uml, 'overview.png'), [(actor, list(range(len(mains))))], mains,
                     [(a, b, g, 'extend', [0], None) for a, b, g in subs])
    S = U.S
    for code, name, group, fname in rieng:
        # khổ 1700 px chữ to như mẫu quốc gia (khuôn phieu-theo-form-quoc-gia/formqg_lib.draw_usecase_qg)
        W, H = 850 * S, 270 * S
        img = Image.new('RGB', (W, H), 'white')
        d = ImageDraw.Draw(img)
        cy = H / 2
        ax, ay = U._actor(d, int(W * 0.17), int(cy - 70 * S), actor, U._f(U.F_BOLD, 15), scale=1.15)
        left, _ = U._usecase(d, int(W * 0.64), cy, int(W * 0.27), int(H * 0.27), '%s %s' % (code, name), group,
                             U._f(U.F_REG, 17))
        d.line([(ax + int(6 * S), ay), (left - int(4 * S), cy)], fill=(148, 163, 184), width=max(2, int(1.4 * S)))
        U._finish(img, os.path.join(scr.uml, fname + '.png'), 1700, kind='usecase')
    return sorted(os.listdir(scr.uml))


# ---------------------------------------------------------------------------------------------- SRS
def build_srs(scr, S, out):
    """S (xem docs/warehouses/gen_srs.py): ten, menu [(chữ, icon)], muc_dich, thuat_ngu, quyen_truoc, quyen_rows,
    ma_tran, quyen_sau, fr [...], quy_tac [(mã, tên, mô tả, phạm vi)], phan5 {'cau_dan', 'rows'}."""
    w = QgWriter(SRS_TPL, SRS_ROLES, body_from=10, cover_replace={'Danh mục quốc gia': S['ten']})

    def h1(text):
        h1_trang_moi(w, text)

    def img(path, cap, width=6.2):
        w.image(path, width=width, caption=cap)
        _keep_next(w)

    def sub(text):
        w.raw('sub', text)
        _keep_with_next(w)

    menu = []
    for i, (text, icon) in enumerate(S['menu']):
        menu.append(('Phân hệ ' if i == 0 else ' => ') + text + ' ')
        if icon:
            menu.append(scr.ic(icon, 0.24))

    h1('Phần 1. Giới thiệu')
    w.h2('1 Mục đích')
    w.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % S['ten'])
    for b in S['muc_dich']:
        w.bullet(b)
    w.h2('2 Thuật ngữ và viết tắt')
    w.table([['Thuật ngữ', 'Mô tả']] + S['thuat_ngu'], widths=[1.3, 3])

    h1('Phần 2. Phân quyền')
    w.h2('1 Danh sách quyền')
    for p in S['quyen_truoc']:
        w.p(p)
    w.table([['Tên quyền', 'Tác dụng trên màn hình']] + S['quyen_rows'], widths=[1.5, 3])
    w.h2('2 Ma trận phân quyền')
    w.table(S['ma_tran'], widths=S.get('ma_tran_widths'))
    for p in S.get('quyen_sau', []):
        w.p(p)

    h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
    w.h2('1 Sơ đồ UML tổng quan')
    img(os.path.join(scr.uml, 'overview.png'), 'Sơ đồ Use Case tổng quan màn %s' % S['ten'], 6.3)
    w.h2('2 Đặc tả chi tiết từng chức năng')
    for i, fr in enumerate(S['fr']):
        if not fr.get('ui') or not fr.get('events'):
            raise ValueError('FR "%s" thiếu bảng giao diện / event — bắt buộc ở mọi chức năng' % fr['ten'])
        n = '2.%d' % (i + 1)
        w.h3('%s %s' % (n, fr['ten']))
        k = 0
        if fr.get('uc'):
            k += 1
            sub('%s.%d Biểu đồ Usecase' % (n, k))
            img(os.path.join(scr.uml, fr['uc'] + '.png'), 'Biểu đồ Use Case — %s' % fr['ten'], 6.2)
        k += 1
        sub('%s.%d Giới thiệu' % (n, k))
        w.clone_texts('qtc', ['Quy tắc chung: ', 'Áp dụng SRS Các quy tắc chung ', QTC_LINK,
                              ' - %s Chỉ bổ sung quy tắc riêng của %s.' % (fr['qtc'], S['ten'])])
        w.table([['Mục', 'Nội dung']] + fr['gioi_thieu'], widths=[1, 3.2])
        k += 1
        sub('%s.%d Layout màn hình' % (n, k))
        w.p('Đường dẫn màn hình:')
        extra = scr.segs(fr.get('menu_them', '')) if fr.get('menu_them') else []
        # khuôn quốc gia: dòng "Menu:" (gạch đầu dòng) rồi dòng đường dẫn có icon — như catalog_v2.build_srs
        w.raw('menu_b', 'Menu: ')
        w.raw('menu', menu + extra)
        if fr.get('ghi_chu_layout'):
            w.p(fr['ghi_chu_layout'])
        for name, cap in fr.get('anh', []):
            img(scr.shot(name), cap, _fit_width(scr.shot(name)))
        k += 1
        sub('%s.%d Mô tả chi tiết giao diện' % (n, k))
        w.table(fr['ui'], widths=fr.get('ui_widths'))
        k += 1
        sub('%s.%d Danh sách event và xử lý event' % (n, k))
        w.table([['STT', 'Event', 'Loại event', 'Xử lý event']] +
                [[str(j + 1)] + e for j, e in enumerate(fr['events'])], widths=[0.5, 1.4, 0.8, 3.5])

    h1('Phần 4. Quy tắc nghiệp vụ')
    w.p('**Quy tắc áp dụng:** Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung '
        'SRS_Các quy tắc chung_VN_1.0. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc '
        'đã có trong SRS quy tắc chung.' % S['ten'])
    j = lambda v: '\n'.join(v) if isinstance(v, (list, tuple)) else v  # noqa: E731
    rows = [['STT', 'Mã quy tắc', 'Tên quy tắc', 'Mô tả', 'Phạm vi áp dụng']]
    for i, q in enumerate(S['quy_tac'], 1):
        assert len(q) == 4 and q[0] == 'BR-%02d' % i, 'BR phải liên tục BR-01, BR-02…: %r' % (q[0],)
        rows.append([str(i), q[0], q[1], j(q[2]), j(q[3])])
    w.table(rows, widths=[0.5, 0.85, 1.3, 2.75, 1.2])

    p5 = S['phan5']
    h1(PHAN5_TITLE)
    if p5.get('cau_dan'):
        w.p(p5['cau_dan'])
    w.table([['STT', 'Nhóm', 'Màn hình', 'Đường dẫn']] +
            [[str(i + 1)] + list(r) for i, r in enumerate(p5['rows'])], widths=[0.5, 1.1, 2.4, 2.4])

    w.rebuild_toc(levels=(1, 2, 3))
    _exclude_toc_heading(w)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    _table_runs_13(w)
    w.save(out)
    force_times_new_roman(out)
    return out


# ---------------------------------------------------------------------------------------------- HDSD (gọn)
def build_hdsd(scr, H, out):
    """H: ten, thuat_ngu, phien_ban, quyen [câu], phan [(tiêu đề PHẦN, [mục])].
    Mục: ('step'|'sub'|'sub2'|'p', chuỗi có {icon:…}) · ('img', tên ảnh, chú thích)."""
    w = QgWriter(HDSD_TPL, HDSD_ROLES, body_from=19, cover_replace={'Danh mục khu vực': H['ten']})
    h1_trang_moi(w, 'TỔNG QUAN')
    w.h2('1. Thuật ngữ sử dụng trong tài liệu')
    w.table([['Thuật ngữ', 'Giải thích']] + H['thuat_ngu'], widths=[2.0, 4.5])
    w.h2('2. Cập nhật tài liệu')
    w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung']] + H['phien_ban'], widths=[0.9, 1.1, 1.5, 3.0])
    w.h2('3. Quyền sử dụng')
    for s in H['quyen']:
        w.p(s)
    w.h2('4. Sơ đồ chức năng tổng quan')
    w.image(os.path.join(scr.uml, 'overview.png'), caption='Sơ đồ chức năng tổng quan màn ' + H['ten'])
    _keep_next(w)
    for i, (title, items) in enumerate(H['phan'], 1):
        h1_trang_moi(w, 'PHẦN %d: %s' % (i, title))
        for it in items:
            kind = it[0]
            if kind == 'img':
                w.image(scr.shot(it[1]), width=_fit_width(scr.shot(it[1]), 6.0), caption=it[2])
                _keep_next(w)
            elif kind == 'p':
                w.p(scr.segs(it[1]))
            else:
                w.raw(kind, scr.segs(it[1]))
    w.rebuild_toc(levels=(1, 2))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    _table_runs_13(w)
    w.save(out)
    force_times_new_roman(out)
    return out


# ---------------------------------------------------------------------------------------------- tự kiểm
W_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def check_docx(path, banned=('quốc gia', 'Quốc gia', 'khu vực', 'Khu vực', 'http://', 'https://')):
    """Kiểm sau khi Word đã cập nhật: mục lục không còn chữ của khuôn, font chỉ Times New Roman,
    mọi run trong bảng 13pt (sz=26). Trả dict kết quả, in cảnh báo."""
    from docx import Document
    d = Document(path)
    body = d.element.body
    res = {}
    # mục lục
    sdt = body.find(W_NS + 'sdt')
    toc = ''.join(t.text or '' for t in sdt.iter(W_NS + 't')) if sdt is not None else ''
    res['toc_banned'] = [b for b in banned if b in toc]
    # chữ thân bài (trừ bìa) không còn chữ của khuôn
    text = '\n'.join(''.join(t.text or '' for t in p.iter(W_NS + 't')) for p in body.iter(W_NS + 'p'))
    res['body_banned'] = [b for b in banned if b in text and b not in ('khu vực', 'Khu vực')]
    # font
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf-8')
        styles = z.read('word/styles.xml').decode('utf-8')
        theme = z.read('word/theme/theme1.xml').decode('utf-8') if 'word/theme/theme1.xml' in z.namelist() else ''
    fonts = set(re.findall(r'w:ascii="([^"]+)"', xml)) | set(re.findall(r'w:ascii="([^"]+)"', styles))
    res['fonts'] = sorted(fonts)
    res['theme_fonts'] = sorted(set(re.findall(r'<a:latin typeface="([^"]*)"', theme)))[:4]
    # cỡ chữ trong bảng — cỡ HIỆU LỰC: run -> style đoạn (chuỗi basedOn) -> style bảng -> mặc định tài liệu
    # (Word lưu lại sẽ bỏ cỡ chữ tường minh trùng mặc định 13pt, nên không đòi sz trên từng run)
    def style_sz(sid, seen=()):
        m = re.search(r'<w:style [^>]*w:styleId="%s".*?</w:style>' % re.escape(sid), styles, re.S)
        if not m or sid in seen:
            return None
        v = re.search(r'<w:rPr>.*?<w:sz w:val="(\d+)"', m.group(0), re.S)
        if v:
            return v.group(1)
        b = re.search(r'<w:basedOn w:val="([^"]+)"', m.group(0))
        return style_sz(b.group(1), seen + (sid,)) if b else None
    dm = re.search(r'<w:docDefaults>.*?<w:sz w:val="(\d+)"', styles, re.S)
    default_sz = dm.group(1) if dm else '20'
    bad = 0
    total = 0
    for tbl in body.iter(W_NS + 'tbl'):
        ts = tbl.find('.//' + W_NS + 'tblStyle')
        tsz = style_sz(ts.get(W_NS + 'val')) if ts is not None else None
        for p in tbl.iter(W_NS + 'p'):
            ps = p.find('.//' + W_NS + 'pStyle')
            psz = style_sz(ps.get(W_NS + 'val')) if ps is not None else style_sz('Normal')
            for r in p.iter(W_NS + 'r'):
                if r.find(W_NS + 't') is None:
                    continue
                total += 1
                rpr = r.find(W_NS + 'rPr')
                sz = rpr.find(W_NS + 'sz') if rpr is not None else None
                eff = sz.get(W_NS + 'val') if sz is not None else (psz or tsz or default_sz)
                if eff != '26':
                    bad += 1
    res['table_runs'] = total
    res['table_runs_not13'] = bad
    ok = not res['toc_banned'] and not res['body_banned'] and fonts <= {'Times New Roman'} and bad == 0
    res['ok'] = ok
    print('  KIỂM %s: %s' % (os.path.basename(path), res))
    return res


def render_pages(pdf, out_dir, pages=None, zoom=1.2):
    """PDF -> PNG từng trang (pymupdf) để xem bằng Read. pages: list số trang (1-based) hoặc None = tất cả."""
    import pymupdf
    os.makedirs(out_dir, exist_ok=True)
    doc = pymupdf.open(pdf)
    paths = []
    for i, pg in enumerate(doc, 1):
        if pages and i not in pages:
            continue
        p = os.path.join(out_dir, 'p%03d.png' % i)
        pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).save(p)
        paths.append(p)
    return paths


def find_pages(pdf, needles):
    """{chuỗi: [trang chứa]} — tìm trang cần soát (Thêm mới, hộp xác nhận, Phần 4, Phần 5…)."""
    import pymupdf
    doc = pymupdf.open(pdf)
    out = {n: [] for n in needles}
    for i, pg in enumerate(doc, 1):
        t = pg.get_text()
        for n in needles:
            if n in t:
                out[n].append(i)
    return out


def contact_sheet(pngs, out, cols=3, width=600):
    """Ghép nhiều trang thành 1 tấm để soát nhanh."""
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert('RGB') for p in pngs]
    ims = [im.resize((width, int(im.height * width / im.width))) for im in ims]
    h = max(im.height for im in ims)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (width + 10), rows * (h + 24)), 'white')
    dr = ImageDraw.Draw(sheet)
    for i, im in enumerate(ims):
        x, y = (i % cols) * (width + 10), (i // cols) * (h + 24)
        sheet.paste(im, (x, y + 20))
        dr.text((x + 4, y + 4), os.path.basename(pngs[i]), fill='red')
    sheet.save(out)
    return out


def shorten_field_icons(scr, prefix='o_', max_w=560):
    """Ảnh ô lọc (o_*) cắt nguyên chiều ngang ô (~800 px) -> chèn cao 0,22" thì chữ bé tí. Giữ phần bên trái (nhãn ô)
    rộng tối đa `max_w` px — như skill hdsd-documenter ("o_timnhanh dài quá ~330px thì cắt ngắn", ảnh chụp 2x)."""
    from PIL import Image
    for f in sorted(os.listdir(scr.icons)):
        if f.startswith(prefix) and f.endswith('.png'):
            p = os.path.join(scr.icons, f)
            im = Image.open(p)
            if im.width > max_w:
                im.crop((0, 0, max_w, im.height)).save(p)
