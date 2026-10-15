# Vá 1 SRS: ý 3 (Người/Ngày tạo, cập nhật) + mục Import (ý 1, 2, 5) theo specs/<id>.json
# python3 patch_srs.py <id> [<id>...]   → out/<id>.docx + out/<id>.log
import json, os, re, sys
import docx
from docxlib import *
from item3 import transform

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

REJ_ALT = ('• Bấm Import khi có dòng không còn hợp lệ so với lúc Validate (ví dụ tên hoặc mã vừa được tạo ở tab khác '
           'hoặc bởi người khác) → hệ thống KHÔNG import dòng nào; cửa sổ Import vẫn giữ nguyên, từng dòng lỗi được tô đỏ '
           'kèm lý do ngay tại dòng đó để người dùng xử lý. Người dùng sửa dòng lỗi rồi Validate lại, hoặc bấm Bỏ dòng lỗi, '
           'sau đó bấm Import.')
REJ_EVENT = ('– Có dòng không còn hợp lệ so với lúc Validate (ví dụ vừa bị tạo trùng tên hoặc mã ở nơi khác) → KHÔNG import '
             'dòng nào, cửa sổ Import giữ nguyên; dòng lỗi được tô đỏ kèm lý do; hiển thị thông báo “Chưa import dòng nào: '
             '<số dòng> dòng không còn hợp lệ — dữ liệu đã thay đổi kể từ lần Validate trước (có thể vừa được tạo ở nơi '
             'khác). Các dòng lỗi được tô đỏ bên dưới — hãy sửa hoặc bấm "Bỏ dòng lỗi" rồi Import lại.”')


ALLOW = ['6. Bấm Import', 'Tải Mau_import', 'Máy chủ kiểm tra lại toàn bộ dòng gửi lên', 'điền dữ liệu từ hàng 3',
         'bỏ qua dòng lỗi', 'Bản ghi tạo từ import luôn ở trạng thái Hoạt động', 'file mẫu không có cột',
         'Tải file Mau_import', 'Bản ghi import luôn', 'Cột #', 'mới ở trạng thái Hoạt động, người tạo là người đang thực hiện',
         'Import: báo', '26 cột theo file mẫu', 'Có dòng lỗi → bỏ các dòng lỗi']
DELETE = ['Dữ liệu đổi giữa Validate và Import', 'Chỉ ghi được một phần', 'Dữ liệu thay đổi giữa lúc Validate và Import']
NOTE_WORDS = ['Bỏ dòng này', 'Code hiện tại', 'KHÔNG khớp', 'Giữ nguyên', 'Chuyển ', 'chờ ', 'Bổ sung:', 'Câu này', 'LẶNG LẼ', 'lưu ý', 'Câu lỗi đang']


def sentence_action(old, new):
    if any(k in old for k in DELETE):
        return 'delete'
    if any(k in new for k in NOTE_WORDS):
        return 'skip'
    if any(k.lower() in old.lower() for k in ALLOW):
        return 'apply'
    return 'skip'


def _mk_run(text, rpr):
    import copy as _c
    from docxlib import _make_run
    return _make_run(text, rpr)


def _mk_br(rpr):
    import copy as _c
    from docxlib import _el
    r = _el('r')
    if rpr is not None:
        r.append(_c.deepcopy(rpr))
    r.append(_el('br'))
    return r


def do_item3(doc, log):
    n = 0
    for tbl in doc.element.body.iter(W('tbl')):
        trs = tbl.findall(W('tr'))
        if not trs:
            continue
        hdr = [txt(c).strip() for c in cells(trs[0])]
        if 'Tên đối tượng' not in hdr:
            continue
        nc = hdr.index('Tên đối tượng')
        dc = len(hdr) - 1
        tc_i = hdr.index('Loại') if 'Loại' in hdr else None
        for tr in trs[1:]:
            cs = cells(tr)
            if len(cs) <= dc:
                continue
            name, desc = txt(cs[nc]).strip(), txt(cs[dc]).strip()
            if len(name) > 45:
                continue
            new = transform(name, desc, txt(cs[tc_i]) if tc_i is not None else '')
            if new and new != desc:
                set_cell_text(cs[dc], new)
                log.append(f'[Ý3] {name}: "{desc}" → "{new}"')
                n += 1
    return n


def row_by_label(tbl, label):
    for tr in tbl.findall(W('tr')):
        cs = cells(tr)
        if cs and txt(cs[0]).strip().lower().startswith(label.lower()):
            return tr
    return None


def do_import(doc, spec, log):
    if not spec.get('has_import'):
        log.append('[Import] màn không có Import — bỏ qua')
        return
    head = spec.get('import_heading') or ''
    rx = re.escape(re.sub(r'^\s*[\d.]+\s*', '', head).strip()) if head else r'import'
    s, e, items = find_section(doc, rx)
    if s is None:
        s, e, items = find_section(doc, r'import')
    if s is None:
        log.append('!! KHÔNG tìm thấy mục Import')
        return
    sec = items[s:e]
    tbls = [x for x in sec if x.tag == W('tbl')]
    intro = next((t for t in tbls if row_by_label(t, 'Dòng sự kiện chính') is not None), None)
    ui = next((t for t in tbls if 'Tên đối tượng' in [txt(c).strip() for c in cells(t.findall(W('tr'))[0])]), None)
    ev = next((t for t in tbls if [txt(c).strip() for c in cells(t.findall(W('tr'))[0])][:2] == ['STT', 'Event']), None)

    # Câu sai so với code (chỉ câu thuộc luồng Import vừa bổ sung; còn lại báo user)
    for ws in spec.get('wrong_sentences') or []:
        old, new = nfc(ws['old']).strip(), nfc(ws['new']).strip()
        act = sentence_action(old, new)
        if act == 'skip':
            log.append('[Bỏ qua câu ngoài phạm vi] ' + old[:90] + ' => ' + new[:90])
            continue
        if act == 'delete':
            new = None
        hit = False
        for x in items[s:e]:
            for p in x.iter(W('p')):
                t = txt_br(p)
                if old and old in t:
                    nt = t.replace(old, new if new is not None else '')
                    lines = [l for l in nt.split('\n')]
                    clean = []
                    for l in lines:
                        l2 = re.sub(r'^(\s*[•–-]\s*){2,}', lambda m: m.group(0).strip()[0] + ' ', l)
                        if new is None and re.fullmatch(r'\s*[•–-]?\s*', l2):
                            continue
                        clean.append(l2)
                    nt = '\n'.join(clean)
                    if not nt.strip():
                        p.getparent().remove(p)
                    else:
                        set_par_text(p, nt)
                    hit = True
                    break
            if hit:
                break
        log.append(('[Sửa câu] ' if hit else '!! không thấy câu: ') + old[:80] + (' → ' + (new or '(xoá)')[:80] if hit else ''))

    # Ý 5: dòng sự kiện chính + ghi lịch sử tạo mới
    if intro is not None:
        tr = row_by_label(intro, 'Dòng sự kiện chính')
        tc = cells(tr)[-1]
        ps = [p for p in tc.findall(W('p')) if txt(p).strip()]
        whole = txt(tc)
        if re.search(r'lịch sử', whole, re.I) and re.search(r'tạo mới|thêm mới', whole, re.I):
            log.append('[Ý5] đã có câu ghi lịch sử — giữ nguyên')
        else:
            last = ps[-1]
            nums = [int(x) for x in re.findall(r'(?:^|\n)\s*(\d+)\.\s', txt_br(tc))]
            num = (max(nums) + 1) if nums else None
            sent = spec['history_sentence'].strip()
            sent = re.sub(r'^\d+\.\s*', '', sent)
            line = (f'{num}. ' if num else '') + sent
            clone_par_after(last, last, line)
            log.append(f'[Ý5] thêm bước: {line}')
        # Ý 1: dòng sự kiện phụ
        tr2 = row_by_label(intro, 'Dòng sự kiện phụ')
        if tr2 is not None:
            tc2 = cells(tr2)[-1]
            if 'KHÔNG import dòng nào' in txt(tc2):
                log.append('[Ý1] dòng sự kiện phụ đã có — giữ nguyên')
            else:
                ps2 = [p for p in tc2.findall(W('p')) if txt(p).strip()] or tc2.findall(W('p'))
                last2 = ps2[-1]
                t_last = txt(last2).strip()
                line = REJ_ALT if t_last.startswith('•') else REJ_ALT.lstrip('• ').strip()
                if t_last.startswith('-') or t_last.startswith('–'):
                    line = '- ' + REJ_ALT.lstrip('• ')
                clone_par_after(last2, last2, line)
                log.append('[Ý1] thêm dòng sự kiện phụ')
        else:
            import copy as _c
            main_tr = row_by_label(intro, 'Dòng sự kiện chính')
            nt = _c.deepcopy(main_tr)
            cs = cells(nt)
            set_cell_text(cs[0], 'Dòng sự kiện phụ')
            set_cell_text(cs[-1], REJ_ALT)
            main_tr.addnext(nt)
            log.append('[Ý1] thêm hàng Dòng sự kiện phụ')
    else:
        log.append('!! không thấy bảng Giới thiệu (Dòng sự kiện chính) trong mục Import')

    # Ý 1: event Bấm Import
    if ev is not None:
        target = None
        for tr in ev.findall(W('tr'))[1:]:
            cs = cells(tr)
            if len(cs) >= 2 and re.match(r'^\s*(Bấm|Nhấn|Click)\s+(nút\s+)?Import\s*$', txt(cs[1]).strip(), re.I):
                target = tr
        if target is None:
            for tr in ev.findall(W('tr'))[1:]:
                cs = cells(tr)
                if len(cs) >= 2 and re.search(r'\bImport\b', txt(cs[1])) and not re.search(r'Excel|file|mẫu', txt(cs[1]), re.I):
                    target = tr
        if target is None:
            log.append('!! không thấy event "Bấm Import"')
        else:
            tc = cells(target)[-1]
            if 'KHÔNG import' in txt(tc):
                log.append('[Ý1] event đã có — giữ nguyên')
            else:
                ps = tc.findall(W('p'))
                during = next((p for p in ps if txt(p).strip().startswith('During')), None)
                after = next((p for p in ps if txt(p).strip().startswith('After')), None)
                body = next((p for p in ps if txt(p).strip() and not re.match(r'^(Before|During|After)', txt(p).strip())), ps[-1])
                one = len([q for q in ps if txt(q).strip()]) == 1 and re.search(r'After:', txt(ps[0]))
                if one:
                    para = [q for q in ps if txt(q).strip()][0]
                    tnode = next(t for t in para.iter(W('t')) if (t.text or '').lstrip().startswith('After'))
                    run = tnode.getparent()
                    rpr = run.find(W('rPr'))
                    has_br = bool(para.findall('.//' + W('br')))
                    newr = _mk_run(REJ_EVENT, rpr)
                    kids = list(run)
                    br_in_run = any(k.tag == W('br') for k in kids[:kids.index(tnode)])
                    if has_br and br_in_run:
                        run.addprevious(_mk_br(rpr))
                        run.addprevious(newr)
                    elif has_br:
                        run.addprevious(newr)
                        run.addprevious(_mk_br(rpr))
                    else:
                        run.addprevious(newr)
                elif during is not None:
                    # chèn sau dòng cuối của khối During (trước After)
                    idx = ps.index(during)
                    anchor = during
                    for p in ps[idx + 1:]:
                        if p is after:
                            break
                        anchor = p
                    clone_par_after(anchor, body, REJ_EVENT)
                elif after is not None:
                    d = clone_par_after(after, after, 'During:')
                    after.addprevious(d)
                    x = clone_par_after(d, body, REJ_EVENT)
                else:
                    clone_par_after(ps[-1], body, REJ_EVENT)
                log.append('[Ý1] thêm xử lý event Bấm Import')
    else:
        log.append('!! không thấy bảng event trong mục Import')

    # Ý 2: bảng cột file mẫu — đặt ngay sau bảng mô tả giao diện của mục Import
    cols = spec.get('columns') or []
    if cols and ui is not None and ev is not None:
        sec_text = ''.join(txt(x) for x in sec)
        if 'Danh sách cột trong file Excel mẫu' in sec_text:
            log.append('[Ý2] đã có bảng cột — giữ nguyên')
        else:
            # đoạn văn thường làm khuôn: đoạn "Đường dẫn màn hình:" / "Menu:" trong mục
            tpl_p = next((x for x in sec if x.tag == W('p') and re.match(r'^(Đường dẫn|Truy cập) màn hình', txt(x).strip())), None)
            if tpl_p is None:
                tpl_p = next(x for x in sec if x.tag == W('p') and txt(x).strip() and not style_of(x).startswith('Heading'))
            fn = spec.get('template_file') or ''
            label = 'Danh sách cột trong file Excel mẫu' + (f' ({fn})' if fn else '') + ':'
            p = clone_par_after(ui, tpl_p, label, bold=True)
            rows = [[str(i + 1), c['name'], c['required'], c['desc']] for i, c in enumerate(cols)]
            clone_table_after(p, ev, ['STT', 'Tên cột', 'Bắt buộc', 'Mô tả'], rows)
            log.append(f'[Ý2] thêm bảng {len(cols)} cột file mẫu')
    elif cols:
        log.append('!! không chèn được bảng cột (thiếu bảng giao diện/event làm khuôn)')

def patch(id_):
    doc = docx.Document(f'drive/{id_}.docx')
    log = []
    n3 = do_item3(doc, log)
    sp = f'specs/{id_}.json'
    if os.path.exists(sp):
        do_import(doc, json.load(open(sp)), log)
    os.makedirs('out', exist_ok=True)
    doc.save(f'out/{id_}.docx')
    open(f'out/{id_}.log', 'w').write('\n'.join(log))
    return n3, log


if __name__ == '__main__':
    for i in sys.argv[1:]:
        n3, log = patch(i)
        bad = [l for l in log if l.startswith('!!')]
        print(i, 'ý3:', n3, '| import:', len([l for l in log if not l.startswith('[Ý3]')]), '| lỗi:', bad)
