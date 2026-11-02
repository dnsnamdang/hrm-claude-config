# -*- coding: utf-8 -*-
"""Bộ dựng SRS + HDSD cho MÀN BÁO CÁO — bọc `danh-muc-kho/docs/_lib_win.py` (KHÔNG sửa file đó: agent khác dùng song song).

Khác `_lib_win.build_srs` / `build_hdsd`:
- SRS: mỗi chức năng có thêm `them` = [(tiêu đề mục, header, rows, widths)] chèn SAU bảng event — dùng cho
  "Cách lấy dữ liệu và giải thích chỉ tiêu" (4 cột) và "Danh sách liên kết / popup mở từ số liệu" (5 cột) theo skill
  srs-documenter (màn báo cáo). Tiêu đề Phần 5 truyền qua S['phan5']['title'].
- HDSD: mục ('table', header, rows, widths) cho PHẦN "ĐỌC BÁO CÁO" (user chốt 02/11/2026: ngoại lệ duy nhất có bảng).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KHO_DOCS = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'danh-muc-kho', 'docs'))
sys.path.insert(0, KHO_DOCS)
import _lib_win as L  # noqa: E402

QgWriter = L.QgWriter


def build_srs(scr, S, out):
    w = QgWriter(L.SRS_TPL, L.SRS_ROLES, body_from=10, cover_replace={'Danh mục quốc gia': S['ten']})

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

    h1('Phần 1. Giới thiệu')
    w.h2('1 Mục đích')
    w.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % S['ten'])
    for b in S['muc_dich']:
        w.bullet(b)
    w.h2('2 Thuật ngữ và viết tắt')
    w.table([['Thuật ngữ', 'Mô tả']] + S['thuat_ngu'], widths=[1.5, 4.8])

    h1('Phần 2. Phân quyền')
    w.h2('1 Danh sách quyền')
    for p in S['quyen_truoc']:
        w.p(p)
    w.table([['Tên quyền', 'Tác dụng trên màn hình']] + S['quyen_rows'], widths=[2.4, 3.9])
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
            raise ValueError('FR "%s" thiếu bảng giao diện / event' % fr['ten'])
        n = '2.%d' % (i + 1)
        w.h3('%s %s' % (n, fr['ten']))
        k = 0
        if fr.get('uc'):
            k += 1
            sub('%s.%d Biểu đồ Usecase' % (n, k))
            img(os.path.join(scr.uml, fr['uc'] + '.png'), 'Biểu đồ Use Case — %s' % fr['ten'], 6.2)
        k += 1
        sub('%s.%d Giới thiệu' % (n, k))
        w.clone_texts('qtc', ['Quy tắc chung: ', 'Áp dụng SRS Các quy tắc chung ', L.QTC_LINK,
                              ' - %s Chỉ bổ sung quy tắc riêng của %s.' % (fr['qtc'], S['ten'])])
        w.table([['Mục', 'Nội dung']] + fr['gioi_thieu'], widths=[1.3, 5.0])
        k += 1
        sub('%s.%d Layout màn hình' % (n, k))
        w.p('Đường dẫn màn hình:')
        extra = scr.segs(fr.get('menu_them', '')) if fr.get('menu_them') else []
        w.raw('menu_b', 'Menu: ')
        w.raw('menu', menu + extra)
        if fr.get('ghi_chu_layout'):
            w.p(fr['ghi_chu_layout'])
        for name, cap in fr.get('anh', []):
            p = scr.shot(name)
            img(p, cap, L._fit_width(p))
        k += 1
        sub('%s.%d Mô tả chi tiết giao diện' % (n, k))
        w.table(fr['ui'], widths=fr.get('ui_widths'))
        k += 1
        sub('%s.%d Danh sách event và xử lý event' % (n, k))
        w.table([['STT', 'Event', 'Loại event', 'Xử lý event']] +
                [[str(j + 1)] + e for j, e in enumerate(fr['events'])], widths=[0.6, 1.5, 0.85, 3.4])
        for title, head, rows, widths, cau_dan in fr.get('them', []):
            k += 1
            sub('%s.%d %s' % (n, k, title))
            if cau_dan:
                w.p(cau_dan)
            w.table([head] + [[str(j + 1)] + list(r) for j, r in enumerate(rows)], widths=widths)

    h1('Phần 4. Quy tắc nghiệp vụ')
    w.p('**Quy tắc áp dụng:** Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung '
        'SRS_Các quy tắc chung_VN_1.0. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc '
        'đã có trong SRS quy tắc chung.' % S['ten'])
    j = lambda v: '\n'.join(v) if isinstance(v, (list, tuple)) else v  # noqa: E731
    rows = [['STT', 'Mã quy tắc', 'Tên quy tắc', 'Mô tả', 'Phạm vi áp dụng']]
    for i, q in enumerate(S['quy_tac'], 1):
        assert len(q) == 4 and q[0] == 'BR-%02d' % i, 'BR phải liên tục: %r' % (q[0],)
        rows.append([str(i), q[0], q[1], j(q[2]), j(q[3])])
    w.table(rows, widths=[0.6, 0.9, 1.3, 2.7, 1.2])

    p5 = S['phan5']
    h1(p5['title'])
    if p5.get('cau_dan'):
        w.p(p5['cau_dan'])
    w.table([['STT', 'Nhóm', 'Màn hình', 'Đường dẫn']] +
            [[str(i + 1)] + list(r) for i, r in enumerate(p5['rows'])], widths=[0.6, 1.0, 2.4, 2.4])

    w.rebuild_toc(levels=(1, 2, 3))
    L._exclude_toc_heading(w)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L._table_runs_13(w)
    w.save(out)
    L.force_times_new_roman(out)
    return out


def build_hdsd(scr, H, out):
    w = QgWriter(L.HDSD_TPL, L.HDSD_ROLES, body_from=19, cover_replace={'Danh mục khu vực': H['ten']})
    L.h1_trang_moi(w, 'TỔNG QUAN')
    w.h2('1. Thuật ngữ sử dụng trong tài liệu')
    w.table([['Thuật ngữ', 'Giải thích']] + H['thuat_ngu'], widths=[2.0, 4.5])
    w.h2('2. Cập nhật tài liệu')
    w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung']] + H['phien_ban'], widths=[0.9, 1.1, 1.5, 3.0])
    w.h2('3. Quyền sử dụng')
    for s in H['quyen']:
        w.p(s)
    w.h2('4. Sơ đồ chức năng tổng quan')
    w.image(os.path.join(scr.uml, 'overview.png'), caption='Sơ đồ chức năng tổng quan màn ' + H['ten'])
    L._keep_next(w)
    for i, (title, items) in enumerate(H['phan'], 1):
        L.h1_trang_moi(w, 'PHẦN %d: %s' % (i, title))
        for it in items:
            kind = it[0]
            if kind == 'img':
                p = scr.shot(it[1])
                w.image(p, width=it[3] if len(it) > 3 else L._fit_width(p, 6.0), caption=it[2])
                L._keep_next(w)
            elif kind == 'table':
                w.table([it[1]] + it[2], widths=it[3])
            elif kind == 'p':
                w.p(scr.segs(it[1]))
            else:
                w.raw(kind, scr.segs(it[1]))
    w.rebuild_toc(levels=(1, 2))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L._table_runs_13(w)
    w.save(out)
    L.force_times_new_roman(out)
    return out
