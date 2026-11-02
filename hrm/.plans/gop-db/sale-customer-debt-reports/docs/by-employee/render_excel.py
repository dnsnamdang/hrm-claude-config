# -*- coding: utf-8 -*-
"""Dựng HTML từ 2 file Excel TẢI VỀ THẬT (excel_tai_ve/) để chụp ảnh bố cục file cho SRS/HDSD (render_excel.js chụp).
Giữ nguyên ô gộp, chữ đậm, định dạng số #,##0 (0 để trống như định dạng của file). Không thêm / bớt dữ liệu."""
import html
import os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'excel_tai_ve')
OUT = os.path.join(HERE, 'hdsd_shots', '_excel_html')
os.makedirs(OUT, exist_ok=True)


def fmt(cell):
    v = cell.value
    if v is None:
        return ''
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if cell.number_format == '0':
            return str(int(v)) if v != '' else ''
        if v == 0:
            return ''
        return '{:,.0f}'.format(v)
    return str(v)


def render(name, out):
    wb = openpyxl.load_workbook(os.path.join(SRC, name))
    ws = wb.active
    span = {}
    skip = set()
    for rng in ws.merged_cells.ranges:
        span[(rng.min_row, rng.min_col)] = (rng.max_row - rng.min_row + 1, rng.max_col - rng.min_col + 1)
        for r in range(rng.min_row, rng.max_row + 1):
            for c in range(rng.min_col, rng.max_col + 1):
                if (r, c) != (rng.min_row, rng.min_col):
                    skip.add((r, c))
    rows = []
    for r in range(1, ws.max_row + 1):
        tds = []
        for c in range(1, ws.max_column + 1):
            if (r, c) in skip:
                continue
            cell = ws.cell(r, c)
            rs, cs = span.get((r, c), (1, 1))
            st = []
            if cell.font and cell.font.bold:
                st.append('font-weight:bold')
            if cell.fill and cell.fill.fgColor and cell.fill.fill_type == 'solid' and cell.fill.fgColor.rgb not in (None, '00000000'):
                st.append('background:#' + str(cell.fill.fgColor.rgb)[-6:])
            al = cell.alignment.horizontal if cell.alignment else None
            if al:
                st.append('text-align:' + ('center' if al == 'center' else al))
            if r <= 2:
                st.append('border:none')
            if cell.font and cell.font.size and r == 1:
                st.append('font-size:%dpx' % int(cell.font.size * 1.3))
            w = ws.column_dimensions[cell.column_letter].width or 10
            attrs = ''
            if rs > 1:
                attrs += ' rowspan="%d"' % rs
            if cs > 1:
                attrs += ' colspan="%d"' % cs
            tds.append('<td%s style="%s;min-width:%dpx">%s</td>' % (attrs, ';'.join(st), int(w * 3.4) if cs == 1 else 0,
                                                                   html.escape(fmt(cell))))
        rows.append('<tr>%s</tr>' % ''.join(tds))
    doc = ('<!doctype html><meta charset="utf-8"><style>body{margin:12px;font-family:Calibri,Arial,sans-serif;font-size:12px;background:#fff}'
           'table{border-collapse:collapse}td{border:1px solid #bfc7d5;padding:3px 6px;white-space:normal;vertical-align:middle}'
           '.sheet{display:inline-block}</style><div class="sheet"><table>%s</table></div>' % ''.join(rows))
    with open(out, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(out)


render('bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien.xlsx', os.path.join(OUT, 'mau1.html'))
render('bao_cao_tong_hop_cong_no_khach_hang_theo_nhan_vien_mau_in.xlsx', os.path.join(OUT, 'mauin.html'))
