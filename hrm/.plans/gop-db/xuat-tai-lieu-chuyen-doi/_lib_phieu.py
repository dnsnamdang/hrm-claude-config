# -*- coding: utf-8 -*-
"""Bộ dựng SRS + HDSD cho các màn PHIẾU (đợt 3 — 7 phiếu nghiệp vụ), chạy trên WINDOWS.

Màn mẫu: `finance-declare-debt-beginning/docs/kh/` (STT 167 Khai báo đầu kỳ công nợ). Phiếu khác: chép 4 script
(`capture.js`, `gen_srs.py`, `gen_hdsd.py`, `gen_testcase.py`) của màn mẫu, đổi khối dữ liệu.

KHÔNG sửa thư viện dùng chung — file này chỉ GỌI LẠI `danh-muc-kho/docs/_lib_win.py` (QgWriter khuôn quốc gia, Word
finalize, tự kiểm, UML) và bổ sung phần riêng của PHIẾU mà khuôn danh mục không có:
  - Phần 1 mục "3 Luồng trạng thái" (bảng Trạng thái | Ý nghĩa | Thao tác được phép | Ai làm + sơ đồ PNG nếu > 2
    trạng thái) — `draw_state_flow()` vẽ sơ đồ.
  - Phần 2 tách 2 bảng: quyền thao tác + quyền PHẠM VI DỮ LIỆU (ai xem phiếu của ai), rồi ma trận.
  - Mỗi chức năng được thêm dòng "Hoặc Menu: ..." (màn nằm ở 2 chỗ menu) và tiêu đề Phần 5 theo SRS màn 27.
  - HDSD dùng thẳng `_lib_win.build_hdsd` (khuôn gọn đã duyệt).

Dữ liệu S cho build_srs (xem finance-declare-debt-beginning/docs/kh/gen_srs.py):
  ten, phan_he ('Tài chính'), menu [(chữ, icon)], menu_khac [chuỗi "Hoặc Menu: ..."], muc_dich [..], thuat_ngu [[a,b]],
  trang_thai {'cau_dan', 'rows' [[trạng thái, ý nghĩa, thao tác được phép, ai làm]], 'anh' (tên PNG trong uml/ hoặc None),
              'ghi_chu' [..]},
  quyen_truoc [..], quyen_rows [[tên quyền, tác dụng]], pham_vi_truoc [..], pham_vi_rows [[thứ tự, tên quyền, phạm vi]],
  ma_tran [[...]], ma_tran_widths, quyen_sau [..], fr [...], quy_tac [(BR-xx, tên, mô tả, phạm vi)], phan5 {cau_dan, rows}.
Mỗi fr: ten, uc (tên PNG sơ đồ riêng | None), uc_ten (chữ trong chú thích), qtc, gioi_thieu [[Mục, Nội dung]],
  menu_them (chuỗi có {icon:..}), hoac_menu [chuỗi] (đường dẫn khác), ghi_chu_layout, anh [(tên ảnh, chú thích)],
  ui (bảng, dòng 0 là tiêu đề), ui_widths, events [[event, loại, xử lý]].
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GOPDB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(GOPDB, 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402  (đồng thời đặt sys.path tới qg_writer, srs_uml_render, tc_engine)
from _lib_win import (Screen, word_finalize, render_pages, find_pages, contact_sheet, draw_uml,  # noqa: E402,F401
                      build_hdsd, shorten_field_icons, NGAY)

PHAN5_TITLE = 'Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu'
TRUOC_LUU = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung SRS_Các quy tắc chung_VN_1.0, '
             'không thực hiện bước After.')

# Cột bảng "Mô tả chi tiết giao diện" hay dùng (khuôn màn 27)
UI6 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Giá trị ban đầu', 'Mô tả']
UI6W = [0.55, 1.35, 0.9, 0.8, 1.0, 2.6]
UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.45, 1.25, 0.85, 0.8, 1.05, 0.8, 2.6]
UI8 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
UI8W = [0.55, 1.1, 0.85, 0.75, 0.95, 0.7, 0.9, 2.2]
UI4 = ['STT', 'Tên đối tượng', 'Loại', 'Mô tả']
UI4W = [0.5, 1.6, 1.0, 3.6]


def ui(header, rows):
    """Bảng giao diện: tự đánh STT."""
    return [header] + [[str(i + 1)] + list(r) for i, r in enumerate(rows)]


# ---------------------------------------------------------------------------------------------- sơ đồ trạng thái
def draw_state_flow(path, states, transitions, title=None, width=2400):
    """Sơ đồ luồng trạng thái PNG (≥1700 px, chữ to như sơ đồ Use Case khuôn quốc gia).

    states: [(mã, nhãn, màu nền '#rrggbb')] — xếp trái → phải theo thứ tự; mã 'start' / 'end' vẽ chấm tròn.
    transitions: [(từ, đến, nhãn mũi tên)] — từ/đến là mã; mũi tên ngược chiều (về bên trái) vẽ cong phía dưới.
    """
    from PIL import Image, ImageDraw, ImageFont
    fdir = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts')
    f_box = ImageFont.truetype(os.path.join(fdir, 'timesbd.ttf'), 40)
    f_lbl = ImageFont.truetype(os.path.join(fdir, 'times.ttf'), 32)
    f_tit = ImageFont.truetype(os.path.join(fdir, 'timesbd.ttf'), 36)
    # chấm đầu / cuối chiếm 1 phần, ô trạng thái chiếm 3 phần bề ngang (chừa chỗ cho chữ trên mũi tên)
    units = [1.0 if c in ('start', 'end') else 3.0 for c, _, _ in states]
    unit = width / sum(units)
    gap = 3.0 * unit * 0.62  # bề rộng tối đa của ô trạng thái
    H = 700
    img = Image.new('RGB', (width, H), 'white')
    d = ImageDraw.Draw(img)
    cy = 300
    box = {}
    acc = 0.0
    for i, (code, label, color) in enumerate(states):
        cx = (acc + units[i] / 2) * unit
        acc += units[i]
        if code in ('start', 'end'):
            r = 22
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill='#111827')
            if code == 'end':
                d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], outline='#111827', width=4)
            box[code] = (cx - r - 8, cy - r, cx + r + 8, cy + r)
            continue
        lines = _wrap(d, label, f_box, gap - 60)
        lh = 48
        bw = max(d.textlength(s, font=f_box) for s in lines) + 60
        bh = lh * len(lines) + 40
        x0, y0 = cx - bw / 2, cy - bh / 2
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=26, fill=color, outline='#334155', width=3)
        for k, s in enumerate(lines):
            d.text((cx - d.textlength(s, font=f_box) / 2, y0 + 20 + k * lh), s, font=f_box, fill='#0f172a')
        box[code] = (x0, y0, x0 + bw, y0 + bh)
    back = 0
    over = 0
    for a, b, label in transitions:
        ax0, ay0, ax1, ay1 = box[a]
        bx0, by0, bx1, by1 = box[b]
        between = [k for k, v in box.items() if k not in (a, b) and v[0] >= ax1 and v[2] <= bx0]
        if bx0 >= ax1 and between:  # sang phải nhưng vượt qua ô khác: vòng phía trên
            over += 1
            yt = min(ay0, by0) - 50 - 60 * (over - 1)
            sx, ex = (ax0 + ax1) / 2, (bx0 + bx1) / 2
            d.line([(sx, ay0 - 4), (sx, yt), (ex, yt), (ex, by0 - 8)], fill='#b91c1c', width=4)
            _arrow(d, (ex, by0 - 8), 'd', '#b91c1c')
            d.text(((sx + ex) / 2 - d.textlength(label, font=f_lbl) / 2, yt - 36), label, font=f_lbl, fill='#991b1b')
            continue
        if bx0 >= ax1:  # sang phải: thẳng
            y = cy
            p0, p1 = (ax1 + 4, y), (bx0 - 6, y)
            d.line([p0, p1], fill='#475569', width=4)
            _arrow(d, p1, 'r')
            lines = _wrap(d, label, f_lbl, p1[0] - p0[0] - 10)
            for k, s in enumerate(lines):
                d.text(((p0[0] + p1[0]) / 2 - d.textlength(s, font=f_lbl) / 2, y - 14 - 34 * (len(lines) - k)), s,
                       font=f_lbl, fill='#1e3a8a')
        else:  # quay lại: vòng phía dưới
            back += 1
            yb = max(ay1, by1) + 60 + 70 * (back - 1)
            sx, ex = (ax0 + ax1) / 2, (bx0 + bx1) / 2
            d.line([(sx, ay1 + 4), (sx, yb), (ex, yb), (ex, by1 + 8)], fill='#b45309', width=4)
            _arrow(d, (ex, by1 + 8), 'u', '#b45309')
            d.text(((sx + ex) / 2 - d.textlength(label, font=f_lbl) / 2, yb + 6), label, font=f_lbl, fill='#92400e')
    if title:
        d.text((width / 2 - d.textlength(title, font=f_tit) / 2, 30), title, font=f_tit, fill='#0f172a')
    # cắt bớt nền trắng dưới
    bbox = Image.eval(img.convert('L'), lambda v: 255 - v).getbbox()
    if bbox:
        img = img.crop((0, max(0, bbox[1] - 30), width, min(H, bbox[3] + 30)))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return path


def _wrap(d, text, font, maxw):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def _arrow(d, p, direction, color='#475569'):
    x, y = p
    s = 16
    pts = {'r': [(x, y), (x - s * 1.6, y - s), (x - s * 1.6, y + s)],
           'u': [(x, y), (x - s, y + s * 1.6), (x + s, y + s * 1.6)],
           'd': [(x, y), (x - s, y - s * 1.6), (x + s, y - s * 1.6)]}[direction]
    d.polygon(pts, fill=color)


# ---------------------------------------------------------------------------------------------- SRS phiếu
def build_srs(scr, S, out):
    from qg_writer import QgWriter
    from catalog_v2 import SRS_ROLES, QTC_LINK
    w = QgWriter(L.SRS_TPL, SRS_ROLES, body_from=10, cover_replace={'Danh mục quốc gia': S['ten']})

    def h1(text):
        L.h1_trang_moi(w, text)

    def img(path, cap, width=6.2):
        w.image(path, width=width, caption=cap)
        L._keep_next(w)

    def sub(text):
        w.raw('sub', text)
        L._keep_with_next(w)

    menu = []
    for i, (text, icon) in enumerate(S['menu']):
        menu.append(('Phân hệ ' if i == 0 else ' => ') + text + ' ')
        if icon:
            menu.append(scr.ic(icon, 0.24))

    # ---- Phần 1
    h1('Phần 1. Giới thiệu')
    w.h2('1 Mục đích')
    w.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s thuộc phân hệ %s, nhằm:' % (S['ten'], S['phan_he']))
    for b in S['muc_dich']:
        w.bullet(b)
    w.h2('2 Thuật ngữ và viết tắt')
    w.table([['Thuật ngữ', 'Mô tả']] + S['thuat_ngu'], widths=[1.3, 3])
    tt = S['trang_thai']
    w.h2('3 Luồng trạng thái')
    if tt.get('cau_dan'):
        w.p(tt['cau_dan'])
    w.table([['Trạng thái', 'Ý nghĩa', 'Thao tác được phép', 'Ai làm']] + tt['rows'], widths=[1.2, 2.0, 1.8, 1.4])
    if tt.get('anh'):
        img(os.path.join(scr.uml, tt['anh'] + '.png'), 'Sơ đồ luồng trạng thái %s' % S['ten_ngan'], 6.2)
    for g in tt.get('ghi_chu', []):
        w.p(g)

    # ---- Phần 2
    h1('Phần 2. Phân quyền')
    w.h2('1 Danh sách quyền')
    for p in S['quyen_truoc']:
        w.p(p)
    w.table([['Tên quyền', 'Tác dụng trên màn hình']] + S['quyen_rows'], widths=[1.6, 3])
    for p in S.get('pham_vi_truoc', []):
        w.p(p)
    if S.get('pham_vi_rows'):
        w.table([['Thứ tự xét', 'Tên quyền', 'Phạm vi dữ liệu']] + S['pham_vi_rows'], widths=[0.8, 2.0, 3.0])
    for p in S.get('pham_vi_sau', []):
        w.p(p)
    w.h2('2 Ma trận phân quyền')
    w.table(S['ma_tran'], widths=S.get('ma_tran_widths'))
    for p in S.get('quyen_sau', []):
        w.p(p)

    # ---- Phần 3
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
            img(os.path.join(scr.uml, fr['uc'] + '.png'), 'Biểu đồ Use Case — %s' % fr.get('uc_ten', fr['ten']), 6.2)
        k += 1
        sub('%s.%d Giới thiệu' % (n, k))
        w.clone_texts('qtc', ['Quy tắc chung: ', 'Áp dụng SRS Các quy tắc chung ', QTC_LINK,
                              ' - %s Chỉ bổ sung quy tắc riêng của %s.' % (fr['qtc'], S['ten'])])
        w.table([['Mục', 'Nội dung']] + fr['gioi_thieu'], widths=[1, 3.2])
        k += 1
        sub('%s.%d Layout màn hình' % (n, k))
        w.p('Đường dẫn màn hình:')
        extra = scr.segs(fr['menu_them']) if fr.get('menu_them') else []
        w.raw('menu_b', 'Menu: ')
        w.raw('menu', menu + extra)
        for h in fr.get('hoac_menu', []):
            w.p(scr.segs(h))
        if fr.get('ghi_chu_layout'):
            w.p(fr['ghi_chu_layout'])
        for name, cap in fr.get('anh', []):
            img(scr.shot(name), cap, L._fit_width(scr.shot(name)))
        k += 1
        sub('%s.%d Mô tả chi tiết giao diện' % (n, k))
        w.table(fr['ui'], widths=fr.get('ui_widths'))
        k += 1
        sub('%s.%d Danh sách event và xử lý event' % (n, k))
        w.table([['STT', 'Event', 'Loại event', 'Xử lý event']] +
                [[str(j + 1)] + e for j, e in enumerate(fr['events'])], widths=[0.5, 1.4, 0.8, 3.5])

    # ---- Phần 4
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

    # ---- Phần 5
    p5 = S['phan5']
    h1(PHAN5_TITLE)
    if p5.get('cau_dan'):
        w.p(p5['cau_dan'])
    w.table([['STT', 'Nhóm', 'Màn hình', 'Đường dẫn']] +
            [[str(i + 1)] + list(r) for i, r in enumerate(p5['rows'])], widths=[0.5, 1.1, 2.4, 2.4])

    w.rebuild_toc(levels=(1, 2, 3))
    L._exclude_toc_heading(w)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    L._table_runs_13(w)
    w.save(out)
    L.force_times_new_roman(out)
    return out


def check_docx(path, extra_banned=()):
    """Tự kiểm sau Word finalize (mục lục sạch chữ khuôn, chỉ Times New Roman, chữ bảng 13pt) + chữ cấm thêm
    (vd 'ERP', 'API'). Trả dict, in cảnh báo."""
    res = L.check_docx(path, banned=('quốc gia', 'Quốc gia', 'khu vực', 'Khu vực', 'http://', 'https://') + tuple(extra_banned))
    return res


def finalize_and_check(docx, pdf, extra_banned=()):
    pages = word_finalize(docx, pdf)
    print('Số trang %s: %s' % (os.path.basename(docx), pages))
    check_docx(docx, extra_banned)
    return pages
