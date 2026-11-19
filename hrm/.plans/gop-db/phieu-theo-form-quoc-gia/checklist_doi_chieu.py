# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu 1 màn với checklist "Mẫu tài liệu.xlsx" của tester (user gửi 02/11/2026).

Checklist lưu ở checklist_mau_tai_lieu.json (cùng thư mục), 2 phần:
  - Testcase : 324 case cần kiểm tra (Nhóm chức năng > Phân nhóm > Case), đánh stt 1..324 theo thứ tự dòng.
  - SRS      : 163 nội dung cần có trong SRS, stt 1..163.

Mỗi màn khai 2 dict trong gen_checklist.py của màn:
    TC_MAP  = {stt: 'TC_03.001, TC_03.004' | 'N/A: <lý do không áp dụng>'}
    SRS_MAP = {stt: '2.5.2; Phần 4 BR-03'    | 'N/A: <lý do không áp dụng>'}
rồi gọi write(...). Hàm ném lỗi nếu:
  - còn stt chưa khai (thiếu là thiếu, không im lặng bỏ qua),
  - TC ID không có trong testcase.xlsx,
  - mục SRS "2.x" / "2.x.y" / "Phần n" không có trong file SRS,
  - N/A không ghi lý do.
Ghi chú lệch đặt trong ngoặc sau tham chiếu: 'TC_09.008 (lệch: rỗng không ra file — đúng theo code)' → ra cột Ghi chú.
Output: "Đối chiếu checklist.xlsx" (2 sheet, giữ bố cục file mẫu + cột kết quả đối chiếu).
"""
import io
import json
import os
import re

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKLIST = json.load(io.open(os.path.join(HERE, 'checklist_mau_tai_lieu.json'), encoding='utf-8'))

THIN = Side(style='thin', color='999999')
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD_FILL = PatternFill('solid', fgColor='D9E2F3')
NA_FILL = PatternFill('solid', fgColor='EDEDED')
WRAP = Alignment(wrap_text=True, vertical='top')


def _tc_ids(path):
    wb = openpyxl.load_workbook(path, read_only=True)
    ids = set()
    for ws in wb:
        for row in ws.iter_rows(values_only=True):
            for v in row[:4]:
                if isinstance(v, str) and re.match(r'^TC[-_][\w.\-]+$', v.strip()):
                    ids.add(v.strip())
    return ids


def _srs_headings(path):
    import docx
    d = docx.Document(path)
    heads = set()
    for p in d.paragraphs:
        t = p.text.strip()
        m = re.match(r'^(2\.\d+(?:\.\d+)?)\s', t)
        if m:
            heads.add(m.group(1))
        m = re.match(r'^Phần (\d+)\.', t)
        if m:
            heads.add('Phần ' + m.group(1))
    return heads


def _check(kind, items, mapping, valid_ref):
    missing = [it['stt'] for it in items if it['stt'] not in mapping]
    assert not missing, '%s: chưa khai stt %s' % (kind, missing)
    extra = sorted(set(mapping) - {it['stt'] for it in items})
    assert not extra, '%s: stt không có trong checklist %s' % (kind, extra)
    errs = []
    for stt, v in mapping.items():
        v = v.strip()
        if v.startswith('N/A'):
            if len(v) < 8 or ':' not in v:
                errs.append('%s #%d: N/A thiếu lý do' % (kind, stt))
            continue
        bad = valid_ref(_split(v)[0])
        if bad:
            errs.append('%s #%d: không tìm thấy %s' % (kind, stt, bad))
    assert not errs, '\n'.join(errs)


def _split(v):
    """'TC_01.001, TC_01.002 (lệch: …)' → ('TC_01.001, TC_01.002', 'lệch: …'). Ghi chú trong ngoặc ra cột Ghi chú."""
    v = v.strip()
    i = v.find('(')
    if i < 0:
        return v, ''
    return v[:i].strip(), v[i:].strip().strip('()').strip()


def _sheet(ws, items, mapping, col_ref, col_note):
    heads = ['STT', 'Nhóm chức năng', 'Phân nhóm', items and ('Case cần kiểm tra' if col_ref == 'TC ID'
                                                               else 'Nội dung cần có trong SRS'), col_ref, col_note]
    ws.append(heads)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    for it in items:
        v = mapping[it['stt']].strip()
        na = v.startswith('N/A')
        ref, note = ('Không áp dụng', v.split(':', 1)[1].strip()) if na else _split(v)
        ws.append([it['stt'], it['nhom'], it['phan'], it['noi_dung'], ref, note])
        for c in ws[ws.max_row]:
            c.border = BOX
            c.alignment = WRAP
            if na:
                c.fill = NA_FILL
    # gộp ô Nhóm / Phân nhóm như file mẫu
    for col in (2, 3):
        start = 2
        for r in range(3, ws.max_row + 2):
            same = (r <= ws.max_row and ws.cell(r, col).value == ws.cell(start, col).value
                    and (col == 2 or ws.cell(r, 2).value == ws.cell(start, 2).value))
            if not same:
                if r - 1 > start:
                    ws.merge_cells(start_row=start, start_column=col, end_row=r - 1, end_column=col)
                start = r
    for col, w in zip('ABCDEF', (6, 26, 22, 48, 30, 50)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = 'A2'


def write(feature_dir, tc_map, srs_map, testcase='testcase.xlsx', srs=None):
    tc_path = os.path.join(feature_dir, testcase)
    srs_path = srs or next(os.path.join(feature_dir, f) for f in os.listdir(feature_dir)
                           if f.startswith('SRS - ') and f.endswith('.docx'))
    ids = _tc_ids(tc_path)
    heads = _srs_headings(srs_path)

    def tc_ref(v):
        bad = [x for x in re.split(r'[,;\s]+', v) if x and x not in ids]
        return ', '.join(bad)

    def srs_ref(v):
        refs = re.findall(r'(?<![\d.])(2\.\d+(?:\.\d+)?)(?![\d.])|(Phần \d+)', v)
        if not refs:
            return 'tham chiếu mục SRS (ghi dạng 2.x / 2.x.y / Phần n): "%s"' % v
        bad = [a or b for a, b in refs if (a or b) not in heads]
        return ', '.join(bad)

    _check('Testcase', CHECKLIST['Testcase'], tc_map, tc_ref)
    _check('SRS', CHECKLIST['SRS'], srs_map, srs_ref)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Testcase'
    _sheet(ws, CHECKLIST['Testcase'], tc_map, 'TC ID', 'Ghi chú')
    _sheet(wb.create_sheet('SRS'), CHECKLIST['SRS'], srs_map, 'Mục trong SRS', 'Ghi chú')
    out = os.path.join(feature_dir, 'Đối chiếu checklist.xlsx')
    wb.save(out)
    na_tc = sum(1 for v in tc_map.values() if v.strip().startswith('N/A'))
    na_srs = sum(1 for v in srs_map.values() if v.strip().startswith('N/A'))
    print('Đối chiếu checklist: Testcase %d có TC / %d không áp dụng; SRS %d có mục / %d không áp dụng -> %s'
          % (len(tc_map) - na_tc, na_tc, len(srs_map) - na_srs, na_srs, out))
    return out
