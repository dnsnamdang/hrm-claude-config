# -*- coding: utf-8 -*-
"""Doi chieu mot file SRS voi BAN MAU `assets/SRS_MAU.docx` — chay duoc doc lap.

    python3 srs_selfcheck.py "<duong dan>/SRS - <Ten man>.docx"

Sinh ra sau su co 2026-09-03: mot phien lam viec dai da sinh SRS bang API CU (so do use case
ve phang, Phan 4 dang doan BR, muc Layout ghi URL) va tester tra ve 3 lan. Nguyen nhan: nguoi
viet doc SKILL.md o dau phien — truoc luc skill duoc cap nhat — roi khong doc lai, va chi doc
CHU trong file mau chu khong mo ANH so do ra xem.

Bo kiem nay DOC THANG ban mau moi lan chay, nen skill doi thi kiem tra doi theo, khong phu
thuoc vao viec nguoi viet co nho hay khong. `SrsDoc.save()` goi ham `check()` nay tu dong.

Tra ve 0 neu dat, 1 neu co loi. Loi in ra kem CACH SUA.
"""
import os
import re
import sys
import zipfile

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ASSETS = os.path.dirname(os.path.abspath(__file__))
MAU = os.path.join(ASSETS, 'SRS_MAU.docx')

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def _txt(el):
    """Doc chu ke ca khi bi boc trong <w:sdt> (file tai tu Google Docs)."""
    return ''.join(t.text or '' for t in el.iter(W + 't')).strip()


def _blocks(doc):
    for c in doc.element.body.iterchildren():
        if c.tag == qn('w:p'):
            yield Paragraph(c, doc)
        elif c.tag == qn('w:tbl'):
            yield Table(c, doc)


def _uml_kinds(path):
    """Doc dau "srs-uml" trong metadata cua moi anh PNG nhung trong file .docx."""
    import io as _io

    from PIL import Image

    kinds = set()
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if not n.startswith('word/media/') or not n.lower().endswith('.png'):
                continue
            try:
                with Image.open(_io.BytesIO(z.read(n))) as im:
                    k = (im.info or {}).get('srs-uml')
            except Exception:                      # anh chup man hinh, khong phai so do
                continue
            if k:
                kinds.add(k)
    return kinds


UI_LONG = 220                       # o Mo ta dai hon muc nay ma khong xuong dong = kho doc


def _ui_row_issues(tbl):
    """Gop y BA 05/10/2026 (SRS Bao cao tong hop CSKH tiem nang) cho bang 'Mo ta chi tiet giao dien':
    icon (i) phai ghi NGUYEN VAN noi dung ngay trong o; o Mo ta nhieu y phai xuong dong;
    ten doi tuong khong dung tu ky thuat 'Bang cay'."""
    out = []
    for r in tbl.rows[1:]:
        cells = r.cells
        if len(cells) < 3:
            continue
        name = _txt(cells[1]._tc)
        # giu xuong dong: cell.text noi cac doan bang \n, w:br cung ra \n
        mota = cells[-1].text.strip()
        if 'bảng cây' in name.lower():
            out.append('"%s": đổi tên thành "Bảng chi tiết báo cáo" (tên nghiệp vụ, không dùng "bảng cây")' % name)
        if re.search(r'ⓘ(?!\s*[:“"])', mota):
            out.append('"%s": nhắc icon ⓘ mà không ghi nội dung — viết `Icon ⓘ: “<nguyên văn>”` ngay trong ô Mô tả'
                       % name)
        if len(mota) > UI_LONG and '\n' not in mota:
            out.append('"%s": ô Mô tả %d ký tự viết liền 1 đoạn — truyền list để mỗi ý 1 dòng' % (name, len(mota)))
    return out


def _profile(path):
    """Rut cac dac trung hinh thuc cua mot file SRS."""
    d = Document(path)
    paras = [p.text.strip() for p in d.paragraphs]
    heads = {}                      # tieu de bang -> so lan xuat hien
    ui_cols = {}                    # bang "Mo ta chi tiet giao dien" -> so cot
    rule_tbl = None
    data_tbls = []                  # bang "Cach lay du lieu" -> bo tieu de
    popup_tbls = []                 # bang "Danh sach popup mo tu so lieu"
    variant_tbls = []               # bang "Cac bien the theo con so bam"
    ui_issues = []                  # loi cach viet o bang giao dien (gop y BA 05/10/2026)
    for b in _blocks(d):
        if not isinstance(b, Table):
            continue
        h = [_txt(c._tc) for c in b.rows[0].cells]
        key = ' | '.join(h)
        heads[key] = heads.get(key, 0) + 1
        if h[:2] == ['STT', 'Tên đối tượng']:
            ui_cols[len(b.columns)] = ui_cols.get(len(b.columns), 0) + 1
            ui_issues.extend(_ui_row_issues(b))
        if h[:2] == ['STT', 'Mã quy tắc']:
            rule_tbl = h
        if h[:2] == ['STT', 'Chỉ tiêu / Cột']:
            data_tbls.append(h)
        if h[:2] == ['STT', 'Bấm vào']:
            popup_tbls.append(h)
        if h[:2] == ['STT', 'Con số / vị trí bấm']:
            variant_tbls.append(h)
    with zipfile.ZipFile(path) as z:
        media = [n for n in z.namelist() if n.startswith('word/media/')]
    return {
        'paras': paras,
        'heads': heads,
        'ui_cols': ui_cols,
        'rule_tbl': rule_tbl,
        'data_tbls': data_tbls,
        'popup_tbls': popup_tbls,
        'variant_tbls': variant_tbls,
        'ui_issues': ui_issues,
        'popup_purpose': sum(1 for t in paras if re.match(r'^\d+\.\d+\.\d+ Mục đích thiết kế popup', t)),
        'mentions_popup': any('popup' in t.lower() for t in paras),
        'report': any(t.startswith('Màn hình: Báo cáo') for t in paras[:6]),
        'menu': sum(1 for t in paras if t.startswith('Menu: ')),
        # dong "Menu:" co it nhat 1 icon inline (form 2026-09-24)
        'menu_icon': sum(1 for p in d.paragraphs if p.text.strip().startswith('Menu: ')
                         and p._p.xpath('.//a:blip')),
        'rule_ref': sum(1 for t in paras if t.startswith('Quy tắc chung: ')),
        'rule_lead': sum(1 for t in paras if t.startswith('Quy tắc áp dụng: ')),
        # Đếm PHẦN TỬ <w:hyperlink> có r:id trong văn bản, KHÔNG đếm quan hệ (rels): python-docx
        # gộp các link trùng URL vào 1 quan hệ, nên file chưa qua Word (save(update_fields=False))
        # bị đếm thiếu và báo lỗi oan (2026-09-24, cả 6 agent sinh song song đều dính).
        'links': len([h for h in d.element.body.iter(
            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hyperlink')
            if h.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]),
        'media': len(media),
        'fn': sum(1 for p in Document(path).paragraphs
                  if p.style.name == 'Heading 3' and re.match(r'^2\.\d+\s', p.text.strip())),
    }


def check(path, verbose=True):
    """So file SRS voi ban mau. Tra ve danh sach loi (rong = dat)."""
    me = _profile(path)
    mau = _profile(MAU)
    errs = []

    # --- 4 diem cua form 2026-08-28 ---
    if me['menu'] < me['fn']:
        errs.append('Mục Layout: chỉ có %d dòng "Menu: " cho %d chức năng. '
                    'Dùng d.layout(menu=MENU + " => Tạo mới", shot=...)' % (me['menu'], me['fn']))
    if me['menu_icon'] < me['menu']:
        errs.append('Chỉ %d/%d dòng "Menu: " có icon. Form 2026-09-24: mỗi chặng kèm icon cắt từ '
                    'giao diện thật — khai d.set_menu_icons({...}) trước khi gọi d.layout().'
                    % (me['menu_icon'], me['menu']))
    if any('URL đầy đủ' in t for t in me['paras']):
        errs.append('Còn dòng "URL đầy đủ" của form 2026-08-17 — form hiện hành ghi đường dẫn '
                    'MENU, bỏ hẳn URL.')
    if me['rule_ref'] < me['fn']:
        errs.append('Chỉ %d/%d mục Giới thiệu có đoạn "Quy tắc chung: ". '
                    'Dùng d.rule_ref("- <nhóm quy tắc>. ...", anchor="list")'
                    % (me['rule_ref'], me['fn']))
    if me['links'] < me['rule_ref']:
        errs.append('Đoạn "Quy tắc chung" phải là HYPERLINK thật sang SRS quy tắc chung '
                    '(%d đoạn nhưng chỉ %d liên kết) — d.rule_ref() tự chèn, đừng viết d.p() tay.'
                    % (me['rule_ref'], me['links']))
    if me['rule_lead'] != 1:
        errs.append('Phần 4 phải mở đầu bằng ĐÚNG 1 câu "Quy tắc áp dụng: " '
                    '(d.rule_ref(..., head="Quy tắc áp dụng", lead=...)); đang có %d.'
                    % me['rule_lead'])
    if me['rule_tbl'] != mau['rule_tbl']:
        errs.append('Phần 4 phải là BẢNG 5 cột %s — dùng d.rule_table([...]), không viết dạng '
                    '"BR-0N — <tên>" + gạch đầu dòng.' % mau['rule_tbl'])

    # --- so do use case tong quan: phai co phan cap ---
    # Moi so do do srs_uml_render sinh ra deu mang dau "srs-uml" trong metadata PNG:
    #   overview-flat      = ban ve phang cua form cu (draw_overview)
    #   overview-hierarchy = ban co phan cap cua form 2026-08-28 (draw_overview2)
    # Doc dau nay chac chan hon doan theo ty le anh — ban phang cung co the rat rong.
    kinds = _uml_kinds(path)
    if 'overview-flat' in kinds:
        errs.append('Sơ đồ tổng quan đang vẽ bằng hàm cũ draw_overview (không có «extend») — '
                    'dùng d.overview_figure2(actors, mains, subs, caption): chức năng thao tác '
                    'nối actor, chức năng PHỤ (tìm kiếm, xem chi tiết…) «extend» vào màn danh sách.')
    elif 'overview-hierarchy' not in kinds:
        errs.append('Không tìm thấy sơ đồ Use Case tổng quan sinh bằng d.overview_figure2() — '
                    'ảnh chèn tay hoặc dùng hàm cũ đều không đạt.')

    if 'usecase-rel' in kinds:
        errs.append('Sơ đồ Use Case của từng chức năng còn vẽ «include»/«extend» — form '
                    '2026-09-24 chỉ vẽ actor + 1 use case: d.uc_figure(code, tên, nhóm, actor=...).')

    # --- bo cot bang giao dien: chi nhan bo cot co trong ban mau ---
    lech = sorted(set(me['ui_cols']) - set(mau['ui_cols']))
    if lech:
        errs.append('Bảng "Mô tả chi tiết giao diện" có bộ cột %s không có trong bản mẫu (mẫu '
                    'dùng %s cột). Chức năng chỉ đọc = 7 cột (required=False), có nhập liệu = 8 '
                    'cột, hộp xác nhận = 6 cột (required=False, scope=False).'
                    % (lech, sorted(mau['ui_cols'])))

    # --- man BAO CAO: bang cach lay du lieu + noi dung icon (quy dinh 2026-10-05) ---
    data_head = ['STT', 'Chỉ tiêu / Cột', 'Cách lấy dữ liệu', 'Nội dung icon ⓘ']
    if me['report'] and not me['data_tbls']:
        errs.append('Màn BÁO CÁO phải có mục "2.x.6 Cách lấy dữ liệu và giải thích chỉ tiêu" cho '
                    'mỗi chức năng hiện số liệu (báo cáo chính, popup danh sách chi tiết) — dùng '
                    'd.data_table([(chỉ tiêu/cột, cách lấy dữ liệu, nội dung icon ⓘ), ...]).')
    for h in me['data_tbls']:
        if h != data_head:
            errs.append('Bảng cách lấy dữ liệu phải đúng 4 cột %s, đang là %s — dùng d.data_table().'
                        % (data_head, h))

    # --- cach viet bang giao dien (gop y BA 05/10/2026) ---
    if me['ui_issues']:
        errs.append('Bảng "Mô tả chi tiết giao diện" viết khó đọc (%d chỗ) — xem mục "Viết bảng giao diện cho '
                    'người đọc" trong SKILL.md:\n    - %s' % (len(me['ui_issues']), '\n    - '.join(me['ui_issues'][:8])
                    + ('\n    - …' if len(me['ui_issues']) > 8 else '')))

    # --- man BAO CAO co popup mo tu so lieu (quy dinh 2026-10-05) ---
    popup_head = ['STT', 'Bấm vào', 'Popup mở ra', 'Mục đích thiết kế', 'Dữ liệu hiển thị']
    variant_head = ['STT', 'Con số / vị trí bấm', 'Tập dòng hiển thị', 'Tiêu đề popup', 'Ô lọc ẩn / cố định']
    if me['report'] and me['mentions_popup']:
        if not me['popup_tbls']:
            errs.append('Báo cáo có popup nhưng thiếu bảng "Danh sách popup mở từ số liệu" ở chức năng báo '
                        'cáo chính — dùng d.popup_table([(bấm vào, popup mở ra, mục đích thiết kế, dữ liệu), ...]).')
        if not me['popup_purpose']:
            errs.append('Báo cáo có popup nhưng không có mục "2.y.n Mục đích thiết kế popup" nào — mỗi LOẠI '
                        'popup là 1 chức năng riêng, có mục này + bảng biến thể (d.popup_variant_table).')
    for h in me['popup_tbls']:
        if h != popup_head:
            errs.append('Bảng popup phải đúng 5 cột %s, đang là %s.' % (popup_head, h))
    for h in me['variant_tbls']:
        if h != variant_head:
            errs.append('Bảng biến thể popup phải đúng 5 cột %s, đang là %s.' % (variant_head, h))

    # --- muc da bo cua form cu ---
    for s in ('Tổng quan', 'Mini-Spec', 'Tiêu chí nghiệm thu', 'Ngoài phạm vi',
              'Chức năng liên quan', 'Route (FE)'):
        if any(s in t for t in me['paras']):
            errs.append('Còn mục đã bỏ của form cũ: "%s".' % s)

    if verbose:
        name = os.path.basename(path)
        print('--- Đối chiếu với bản mẫu %s' % os.path.basename(MAU))
        print('    %s: %d chức năng | Menu %d | Quy tắc chung %d | hyperlink %d | '
              'bảng giao diện %s | Phần 4 %s%s'
              % (name, me['fn'], me['menu'], me['rule_ref'], me['links'],
                 dict(sorted(me['ui_cols'].items())),
                 'bảng 5 cột' if me['rule_tbl'] == mau['rule_tbl'] else 'SAI',
                 (' | bảng cách lấy dữ liệu %d | bảng popup %d | mục đích popup %d'
                  % (len(me['data_tbls']), len(me['popup_tbls']), me['popup_purpose']))
                 if me['report'] else ''))
        if errs:
            print('!!! %d điểm chưa đúng bản mẫu:' % len(errs))
            for e in errs:
                print('  - %s' % e)
        else:
            print('    => khớp bản mẫu.')
    return errs


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    bad = 0
    for f in sys.argv[1:]:
        bad += 1 if check(f) else 0
    sys.exit(1 if bad else 0)
