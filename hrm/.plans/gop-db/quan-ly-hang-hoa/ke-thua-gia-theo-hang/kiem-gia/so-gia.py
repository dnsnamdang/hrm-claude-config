#!/usr/bin/env python3
"""Ghép 2 lần chụp giá (chup-gia.sql) thành file Excel giá cũ / giá mới — mỗi công ty 1 tab + tab Tổng hợp.

    python3 so-gia.py truoc.tsv[.gz] sau.tsv[.gz] -o so-gia-TPHP.xlsx [--tat-ca]

Mặc định chỉ ghi dòng ĐÁNG XEM: giá trị đổi, hoặc lệch kỳ vọng, hoặc đổi trạng thái kế thừa. `--tat-ca` ghi mọi dòng.
Kỳ vọng (hàng kế thừa ở bản SAU) = dòng nguồn × hệ số k của bản SAU, đúng luật InheritedPriceSync::scaledPriceSql /
scaledCoefficientSql: giá — k = 1 hoặc giá ≤ 1 giữ nguyên, còn lại max(giá, làm tròn(giá × k / 1000) × 1000);
hệ số giá — min(làm tròn(hệ số × k, 2), 999.99); ĐMGG + 3 cờ sửa tay chép nguyên.
"""
import argparse
import csv
import gzip
import sys
from collections import OrderedDict, defaultdict
from decimal import Decimal, ROUND_HALF_UP

from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

MODE_TEXT = {'1': 'Tự xây dựng giá bán riêng theo công ty', '2': 'Kế thừa giá bán theo công ty quản lý hàng'}
NUM_COLS = ('price', 'coefficient', 'sale_max_percent')
FLAG_COLS = ('is_manual_price_online', 'is_manual_coefficient_online', 'is_manual_sale_max_percent_online')
COL_TEXT = {'price': 'giá', 'coefficient': 'hệ số giá', 'sale_max_percent': 'ĐMGG', 'flags': 'cờ sửa tay'}
ONE, THOUSAND, CENT, CAP = Decimal(1), Decimal(1000), Decimal('0.01'), Decimal('999.99')


def unescape(v):
    if v == 'NULL':
        return None
    if '\\' not in v:
        return v
    out, i = [], 0
    while i < len(v):
        ch = v[i]
        if ch == '\\' and i + 1 < len(v):
            out.append({'t': '\t', 'n': '\n', '0': '\0', '\\': '\\'}.get(v[i + 1], v[i + 1]))
            i += 2
        else:
            out.append(ch)
            i += 1
    return ''.join(out)


def load(path):
    opener = gzip.open if path.endswith('.gz') else open
    rows = OrderedDict()
    with opener(path, 'rt', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        head = next(reader)
        if 'product_unit_id' not in head:
            sys.exit(f'{path}: không phải file xuất từ chup-gia.sql (thiếu dòng tiêu đề — nhớ chạy mysql với -B, KHÔNG -N)')
        for raw in reader:
            r = dict(zip(head, map(unescape, raw)))
            rows[(r['cty'], r['product_unit_id'], r['price_type_id'])] = r
    return rows


def dec(v):
    return None if v is None or v == '' else Decimal(v)


def expected(after):
    """Giá trị kỳ vọng của 1 dòng kế thừa ở bản SAU; None khi không kế thừa / thiếu dòng nguồn"""
    if after is None or after['ke_thua'] != '1' or after['src_price'] is None:
        return None
    k = dec(after['he_so_k'])
    p = dec(after['src_price'])
    if k == ONE or p <= ONE:
        price = p
    else:
        price = max(p, (p * k / THOUSAND).quantize(ONE, ROUND_HALF_UP) * THOUSAND)
    c = dec(after['src_coefficient'])
    coef = c if k == ONE else min((c * k).quantize(CENT, ROUND_HALF_UP), CAP)
    return {'price': price, 'coefficient': coef, 'sale_max_percent': dec(after['src_sale_max_percent']),
            'flags': flags(after, 'src_')}


def flags(r, prefix=''):
    return None if r is None else '/'.join(r[prefix + c] or '0' for c in FLAG_COLS)


def inherit_text(r):
    if r is None:
        return ''
    return 'Kế thừa' if r['ke_thua'] == '1' else 'Tự xây dựng giá'


def factor_text(r):
    if r is None or r['ke_thua'] != '1':
        return None
    return float(dec(r['he_so_k']))


HEADERS = [
    ('Mã hàng', 30), ('Tên hàng', 40), ('Hãng', 28), ('ĐVT', 9), ('Loại giá', 20), ('Cty nguồn', 10),
    ('Kế thừa trước', 15), ('Kế thừa sau', 15), ('Hệ số k trước', 11), ('Hệ số k sau', 11),
    ('Giá cũ', 15), ('Giá mới', 15), ('Chênh lệch', 14), ('Giá nguồn', 15), ('Giá kỳ vọng', 15),
    ('Hệ số giá cũ', 11), ('Hệ số giá mới', 11), ('Hệ số giá kỳ vọng', 12),
    ('ĐMGG cũ', 10), ('ĐMGG mới', 10), ('ĐMGG kỳ vọng', 11),
    ('Cờ sửa tay cũ', 12), ('Cờ sửa tay mới', 12), ('Kết quả', 34),
]
MONEY = {'Giá cũ', 'Giá mới', 'Chênh lệch', 'Giá nguồn', 'Giá kỳ vọng'}
RATE = {'Hệ số k trước', 'Hệ số k sau', 'Hệ số giá cũ', 'Hệ số giá mới', 'Hệ số giá kỳ vọng', 'ĐMGG cũ', 'ĐMGG mới', 'ĐMGG kỳ vọng'}

THIN = Side(style='thin', color='FFBFBFBF')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD_FILL = PatternFill('solid', fgColor='FFB8CCE4')
BAD_FILL = PatternFill('solid', fgColor='FFFDE2E2')
CHANGE_FILL = PatternFill('solid', fgColor='FFFFF4D6')
FONT = Font(name='Calibri', size=11)
BOLD = Font(name='Calibri', size=11, bold=True)


def classify(before, after, exp):
    """(kết quả, đáng xem?, lệch?)"""
    if before is None:
        return 'Chỉ có ở bản SAU (hàng mới vào Đang KD)', True, False
    if after is None:
        return 'Chỉ có ở bản TRƯỚC (hàng thôi Đang KD)', True, False
    changed = [c for c in NUM_COLS if dec(before[c]) != dec(after[c])]
    if flags(before) != flags(after):
        changed.append('flags')
    moved = before['ke_thua'] != after['ke_thua'] or (after['ke_thua'] == '1' and before['he_so_k'] != after['he_so_k'])
    if after['ke_thua'] == '1':
        if exp is None:
            return 'LỆCH: thiếu dòng giá ở công ty nguồn', True, True
        bad = [c for c in NUM_COLS if dec(after[c]) != exp[c]]
        if flags(after) != exp['flags']:
            bad.append('flags')
        if bad:
            return 'LỆCH kỳ vọng: ' + ', '.join(COL_TEXT[c] for c in bad), True, True
        if changed:
            return 'Khớp — đổi ' + ', '.join(COL_TEXT[c] for c in changed), True, False
        return 'Khớp — không đổi', moved, False
    if changed:
        return 'Tự xây dựng giá — đổi ' + ', '.join(COL_TEXT[c] for c in changed) + ' (không do cài đặt?)', True, False
    return 'Tự xây dựng giá — không đổi', moved, False


def cell(ws, value, fmt=None, fill=None, font=FONT):
    c = WriteOnlyCell(ws, value=value)
    c.font, c.border = font, BORDER
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    return c


def num(v):
    return None if v is None else float(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('truoc')
    ap.add_argument('sau')
    ap.add_argument('-o', '--out', default='so-gia.xlsx')
    ap.add_argument('--tat-ca', action='store_true', help='ghi mọi dòng, kể cả dòng không đổi')
    a = ap.parse_args()

    before, after = load(a.truoc), load(a.sau)
    keys = list(before.keys()) + [k for k in after.keys() if k not in before]
    by_cty = defaultdict(list)
    for k in keys:
        by_cty[k[0]].append(k)

    wb = Workbook(write_only=True)
    summary = wb.create_sheet('Tổng hợp')
    sheets = {}
    stats = OrderedDict()
    for cty in sorted(by_cty):
        ws = wb.create_sheet(cty[:31])
        for i, (_, w) in enumerate(HEADERS, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = 'C2'
        ws.append([cell(ws, h, font=BOLD, fill=HEAD_FILL) for h, _ in HEADERS])
        sheets[cty] = ws
        st = stats[cty] = defaultdict(int)
        modes = [None, None]
        written = 0
        for key in by_cty[cty]:
            b, af = before.get(key), after.get(key)
            r = af or b
            if b and modes[0] is None:
                modes[0] = b['mode']
            if af and modes[1] is None:
                modes[1] = af['mode']
            exp = expected(af)
            result, notable, bad = classify(b, af, exp)
            st['dong'] += 1
            if b and af and b['price'] is not None and dec(b['price']) != dec(af['price']):
                st['doi_gia'] += 1
                st.setdefault('ma_doi', set()).add(r['product_id'])
            if bad:
                st['lech'] += 1
            if b and af and b['ke_thua'] != af['ke_thua']:
                st['sang_ke_thua' if af['ke_thua'] == '1' else 'sang_tu_tinh'] += 1
            if af and af['ke_thua'] == '1':
                st['ke_thua_sau'] += 1
            if not (notable or a.tat_ca):
                continue
            written += 1
            old_p, new_p = (dec(b['price']) if b else None), (dec(af['price']) if af else None)
            fill = BAD_FILL if bad else (CHANGE_FILL if old_p != new_p else None)
            values = [
                r['ma_hang'], r['ten_hang'], r['hang'], r['dvt'], r['loai_gia'], r['cty_nguon'],
                inherit_text(b), inherit_text(af), factor_text(b), factor_text(af),
                num(old_p), num(new_p), num(new_p - old_p) if old_p is not None and new_p is not None else None,
                num(dec(af['src_price'])) if af else None, num(exp['price']) if exp else None,
                num(dec(b['coefficient'])) if b else None, num(dec(af['coefficient'])) if af else None,
                num(exp['coefficient']) if exp else None,
                num(dec(b['sale_max_percent'])) if b else None, num(dec(af['sale_max_percent'])) if af else None,
                num(exp['sale_max_percent']) if exp else None,
                flags(b), flags(af), result,
            ]
            row = []
            for (h, _), v in zip(HEADERS, values):
                fmt = '#,##0' if h in MONEY else ('0.00' if h in RATE else None)
                row.append(cell(ws, v, fmt, fill if h in ('Giá mới', 'Kết quả') else None))
            ws.append(row)
        st['ghi'] = written
        st['mode_truoc'], st['mode_sau'] = modes
        if written:
            ws.auto_filter.ref = f'A1:{get_column_letter(len(HEADERS))}{written + 1}'

    sum_head = [('Công ty', 10), ('Cách cài TRƯỚC', 40), ('Cách cài SAU', 40), ('Số dòng giá (mã × ĐVT × loại giá)', 18),
                ('Dòng kế thừa (sau)', 14), ('Dòng chuyển sang kế thừa', 14), ('Dòng chuyển sang tự tính', 14),
                ('Dòng đổi giá', 12), ('Số mã đổi giá', 12), ('Dòng LỆCH kỳ vọng', 14), ('Dòng ghi ở tab', 12)]
    for i, (_, w) in enumerate(sum_head, 1):
        summary.column_dimensions[get_column_letter(i)].width = w
    summary.append([cell(summary, h, font=BOLD, fill=HEAD_FILL) for h, _ in sum_head])
    for cty, st in stats.items():
        vals = [cty, MODE_TEXT.get(st['mode_truoc'], ''), MODE_TEXT.get(st['mode_sau'], ''), st['dong'], st['ke_thua_sau'],
                st['sang_ke_thua'], st['sang_tu_tinh'], st['doi_gia'], len(st.get('ma_doi', ())), st['lech'], st['ghi']]
        summary.append([cell(summary, v, '#,##0' if isinstance(v, int) else None,
                             BAD_FILL if j == 9 and v else None) for j, v in enumerate(vals)])
    summary.append([])
    for line in ['Tab công ty: mặc định chỉ có dòng ĐÁNG XEM (đổi giá trị / lệch / đổi trạng thái kế thừa); chạy --tat-ca để có mọi dòng.',
                 'Kỳ vọng = giá công ty nguồn ở bản SAU × hệ số k, làm tròn 1,000 đ, không thấp hơn giá nguồn, giá ≤ 1 đ giữ nguyên;'
                 ' hệ số giá × k (2 số lẻ); ĐMGG + cờ sửa tay chép nguyên.',
                 'Nền đỏ = LỆCH kỳ vọng (gửi file cho dev, KHÔNG sửa tay giá) · nền vàng = giá đổi.',
                 'Cờ sửa tay = giá/hệ số/ĐMGG online (0/1).']:
        summary.append([cell(summary, line, font=FONT)])
    wb.save(a.out)
    for cty, st in stats.items():
        print(f"{cty}: {st['dong']:,} dòng · đổi giá {st['doi_gia']:,} dòng / {len(st.get('ma_doi', ())):,} mã · "
              f"lệch {st['lech']:,} · ghi {st['ghi']:,} dòng")
    print('⇒', a.out)
    return 1 if any(st['lech'] for st in stats.values()) else 0


if __name__ == '__main__':
    sys.exit(main())
