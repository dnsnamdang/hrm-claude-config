"""Port logic edit.vue sang Python (theo đúng hàm JS) rồi so với giá trị Excel đã recalc bằng LibreOffice."""
import sys, math
sys.path.insert(0, '')
from openpyxl import load_workbook

PATH = sys.argv[1]
wb = load_workbook(PATH, data_only=True)


def jround(x, p):  # Math.round(x*10^p)/10^p
    f = 10 ** p
    return math.floor(x * f + 0.5) / f


A = [  # code, type, qty, est, quoted, vat, parentIdx
    ('TD', 'cha', 2, None, 30000000, 10),
    ('BT', 'con', 2, 6500000, 8000000, None),
    ('VT', 'con', 2, 3200000, 4000000, None),
    ('CB', 'doc', 5, 1200000, 1650000, 8),
    ('CAP', 'doc', 100, 25000, 35000, 10),
]
SV = [('DV', 1, 5000000, 8000000, 8, 1), ('CP', 1, 2000000, 2500000, 8, 0)]
SHIP_IMP, SHIP_COST, SHIP_VATP = 1500000, 2000000, 8


def model(mode):
    prec = 0
    prods = []
    for code, t, q, e, s, v in A:
        prods.append(dict(code=code, t=t, qty=q, est=e or 0, quoted=s, vat=v or 0, da=0, alloc=0))
    # roll-up cha (refreshParentRollups)
    p = prods[0]
    p['est'] = jround((6500000 * 2 + 3200000 * 2) / p['qty'], prec)
    parents = [x for x in prods if x['t'] != 'con']
    svcs = [dict(code=c, qty=q, est=e, quoted=s, vat=v, rev=r, da=0, alloc=0) for c, q, e, s, v, r in SV]
    ship_disc = 0
    if mode == 1:
        prods[0]['da'] = jround(30000000 * 5 / 100, 2)      # onDiscountPercentInput
        prods[3]['da'] = 50000
        svcs[0]['da'] = jround(8000000 * 10 / 100, 2)
        ship_disc = jround(SHIP_COST * 10 / 100, 2)
    total_sale = sum(x['quoted'] * x['qty'] for x in parents) + sum(s['quoted'] * s['qty'] for s in svcs)
    tqd = 0
    if mode == 2:
        tqd = jround((total_sale + SHIP_COST) * 3 / 100, 2) + 500000
        # autoAllocationMap — largest remainder theo xu
        lines = [('P' + x['code'], x['quoted'] * x['qty']) for x in parents] + [('S' + s['code'], s['quoted'] * s['qty']) for s in svcs] + [('SHIP', SHIP_COST)]
        grand = sum(v for _, v in lines)
        cents = round(tqd * 100)
        al = []
        for k, v in lines:
            raw = cents * (v / grand)
            al.append([k, math.floor(raw), raw - math.floor(raw)])
        rem = cents - sum(a[1] for a in al)
        for a in sorted(al, key=lambda a: -a[2])[:rem]:
            a[1] += 1
        amap = {k: c / 100 for k, c, _ in al}
        for x in parents:
            x['alloc'] = amap['P' + x['code']]
        for s in svcs:
            s['alloc'] = amap['S' + s['code']]
        ship_disc = amap['SHIP']

    def after(x):
        sale = x['quoted'] * x['qty']
        if mode == 1:
            return sale - x['da'] * x['qty']
        if mode == 2:
            return sale - x['alloc']
        return sale

    rows = {}
    for x in parents + svcs:
        imp = x['est'] * x['qty']
        a = after(x)
        rows[x['code']] = dict(gn=x['est'], ttn=imp, ttb=a, tsln=None if imp <= 0 else jround((a - imp) / imp * 100, 2),
                               tvat=a * x['vat'] / 100, tsv=a + a * x['vat'] / 100)
    g = {k: dict(nhap=0, tv=0, ck=0, vat=0) for k in ('hh', 'dv', 'cp', 'vc')}
    for x in parents:
        g['hh']['nhap'] += x['est'] * x['qty']; g['hh']['tv'] += x['quoted'] * x['qty']
        g['hh']['ck'] += x['quoted'] * x['qty'] - after(x); g['hh']['vat'] += rows[x['code']]['tvat']
    for s in svcs:
        b = g['dv'] if s['rev'] else g['cp']
        b['nhap'] += s['est'] * s['qty']; b['tv'] += s['quoted'] * s['qty']
        b['ck'] += s['quoted'] * s['qty'] - after(s); b['vat'] += after(s) * s['vat'] / 100
    g['vc'] = dict(nhap=SHIP_IMP, tv=SHIP_COST, ck=ship_disc, vat=(SHIP_COST - ship_disc) * SHIP_VATP / 100)
    for b in g.values():
        b['sck'] = b['tv'] - b['ck']; b['sv'] = b['sck'] + b['vat']
    tong = {k: sum(b[k] for b in g.values()) for k in ('nhap', 'tv', 'ck', 'sck', 'vat', 'sv')}
    m_before = jround((tong['tv'] - tong['nhap']) / tong['nhap'] * 100, 2)
    m_after = jround((tong['sck'] - tong['nhap']) / tong['nhap'] * 100, 2)
    lvV = 1 if tong['sck'] < 1e9 else (2 if tong['sck'] < 2e10 else 3)
    lvM = 1 if m_after >= 35 else (2 if m_after >= 20 else 3)
    return rows, g, tong, m_before, m_after, max(lvV, lvM), tqd


SHEETS = {0: 'Không giảm giá', 1: 'Giảm giá mặt hàng', 2: 'Giảm giá tổng'}
bad = 0


def chk(label, got, exp, tol=0.011):
    global bad
    ok = (got is None and exp is None) or (isinstance(got, (int, float)) and exp is not None and abs(got - exp) <= tol)
    if not ok:
        bad += 1
    print(f"  {'OK ' if ok else 'SAI'} {label}: excel={got} app={exp}")


for mode, name in SHEETS.items():
    ws = wb[name]
    print('=====', name)
    hdr = {ws.cell(5, c).value: c for c in range(1, ws.max_column + 1)}
    rows, g, tong, mb, ma, lv, tqd = model(mode)
    for r in range(8, ws.max_row + 1):
        code = ws.cell(r, hdr['Mã']).value
        key = {'TD-01': 'TD', 'CB-AS': 'CB', 'CAP-DK': 'CAP', 'DV-LD': 'DV', 'CP-QL': 'CP'}.get(code)
        if not key:
            continue
        exp = rows[key]
        for col, k in (('Giá nhập', 'gn'), ('Thành tiền nhập', 'ttn'), ('Thành tiền bán', 'ttb'), ('Tiền VAT', 'tvat'), ('Thành tiền sau VAT', 'tsv')):
            chk(f'{code} {col}', ws.cell(r, hdr[col]).value, exp[k])
        v = ws.cell(r, hdr['Tỷ suất LN']).value
        chk(f'{code} Tỷ suất LN(%)', None if v == '—' else round(v * 100, 2), exp['tsln'], 0.001)
    # bảng tổng hợp: tìm dòng "Tổng giá trị báo giá"
    for r in range(1, ws.max_row + 1):
        if ws.cell(r, 1).value in ('I', 'II', 'III', 'IV', 'V') and ws.cell(r, 2).value in ('Hàng hoá', 'Dịch vụ', 'Chi phí', 'Chi phí vận chuyển', 'Tổng giá trị báo giá'):
            key = {'Hàng hoá': 'hh', 'Dịch vụ': 'dv', 'Chi phí': 'cp', 'Chi phí vận chuyển': 'vc'}.get(ws.cell(r, 2).value)
            exp = g[key] if key else tong
            keys = ['nhap', 'tv'] + (['ck', 'sck'] if mode else []) + ['vat', 'sv']
            for i, k in enumerate(keys):
                chk(f'TH {ws.cell(r, 2).value} {k}', ws.cell(r, 3 + i).value, exp[k])
        lab = ws.cell(r, 2).value
        if lab == 'Tỷ suất LN trước giảm giá':
            chk('TSLN trước GG', round(ws.cell(r, 4).value * 100, 2), mb, 0.001)
        if lab == 'Tỷ suất LN (sau giảm giá)':
            chk('TSLN sau GG', round(ws.cell(r, 4).value * 100, 2), ma, 0.001)
        if lab == 'Cấp duyệt (dự kiến)':
            chk('Cấp duyệt', ws.cell(r, 4).value, lv, 0)
        if lab == 'Tổng giảm giá':
            chk('Tổng GG', ws.cell(r, 7).value, tqd)
        if lab == 'Còn phải phân bổ (phải = 0)':
            chk('Còn phải phân bổ', ws.cell(r, 7).value, 0, 0.05)
    # lỗi công thức
    errs = [c.coordinate + '=' + str(c.value) for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith('#') and c.value != '#']
    print('  Lỗi công thức:', errs[:10] or 'không')
    bad += len(errs)
print('TỔNG SAI:', bad)
