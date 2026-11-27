# -*- coding: utf-8 -*-
"""Sinh các khối TSV (cột A..I) để CHÈN vào tab 52 trên Google Sheet, giữ nguyên bố cục + 19 case cũ (user chốt 27/11).

Vị trí (sau khi chèn từ dưới lên): khối A = dòng 20..43 (24), khối B = 47..62 (16), 10.011 = 67, Phân quyền = 72..73.
Ô sửa: I8 (TC_03.001), D14:I14 (TC_03.007), I64 (TC_10.001); ghi chú cột M cùng dòng.
"""
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_testcase_11643_v3 as v3  # noqa: E402

OUTDIR = sys.argv[1]
MOD = 'Giao chỉ tiêu KD theo phòng ban'


def fix(r):
    r = list(r[:9])
    r[8] = r[8].replace('-   ', '- ')
    return r


def sec(label):
    return ['', '', label] + [''] * 6


def with_ab(rows, b):
    rows = [fix(x) for x in rows]
    rows[0][0] = MOD
    rows[0][1] = b
    return rows


S = {g: rows for g, _, rows in v3.SEC}
new_only = lambda rows: [r for r in rows if r[2] not in v3.OLD]  # noqa: E731

blockA = ([fix(r) for r in new_only(S['THÊM MỚI'])]
          + [sec('II. THÊM MỚI — CHỌN PHÒNG BAN / BỘ PHẬN THEO THỊ TRƯỜNG ĐÃ CHIA')]
          + with_ab(S['THÊM MỚI — CHỌN PHÒNG BAN / BỘ PHẬN THEO THỊ TRƯỜNG ĐÃ CHIA'], 'CHỌN PHÒNG BAN / BỘ PHẬN')
          + [sec('III. THÊM MỚI — THỐNG KÊ DÒNG TỈNH/TP & TOÀN PHIẾU')]
          + with_ab(S['THÊM MỚI — THỐNG KÊ DÒNG TỈNH/TP & TOÀN PHIẾU'], 'THỐNG KÊ DÒNG TỈNH/TP & TOÀN PHIẾU'))
blockB = ([fix(r) for r in new_only(S['CHỈNH SỬA'])]
          + [sec('V. GỬI DUYỆT')] + with_ab(S['GỬI DUYỆT'], 'GỬI DUYỆT')
          + [sec('VI. DUYỆT / TỪ CHỐI / HỦY DUYỆT / HỦY PHIẾU')]
          + with_ab(S['DUYỆT / TỪ CHỐI / HỦY DUYỆT / HỦY PHIẾU'], 'DUYỆT / TỪ CHỐI / HỦY DUYỆT / HỦY PHIẾU')
          + [sec('VII. LỊCH SỬ THAY ĐỔI')] + with_ab(S['LỊCH SỬ THAY ĐỔI'], 'LỊCH SỬ THAY ĐỔI'))
blockC = [fix(r) for r in new_only(S['XEM CHI TIẾT PHIẾU'])]
blockD = [sec('XI. PHÂN QUYỀN')] + with_ab(S['PHÂN QUYỀN'], 'PHÂN QUYỀN')
assert (len(blockA), len(blockB), len(blockC), len(blockD)) == (24, 16, 1, 2), (len(blockA), len(blockB), len(blockC), len(blockD))


def tsv(rows):
    q = lambda s: '"' + str(s).replace('"', '""') + '"'  # noqa: E731
    return '\n'.join('\t'.join(q(c) for c in r) for r in rows)


upd = {
    'I8': v3.U_03_001[8],
    'D14': v3.U_03_007[3], 'G14': v3.U_03_007[6], 'H14': v3.U_03_007[7], 'I14': v3.U_03_007[8],
    'I64': v3.U_10_001[8],
    'M8': v3.U_03_001[12], 'M14': v3.U_03_007[12], 'M64': v3.U_10_001[12],
}
for name, rows in [('A', blockA), ('B', blockB), ('C', blockC), ('D', blockD)]:
    open(os.path.join(OUTDIR, 'blk%s.tsv' % name), 'w', encoding='utf-8').write(tsv(rows))
json.dump(upd, open(os.path.join(OUTDIR, 'upd.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sec_rows = [20 + i for i, r in enumerate(blockA) if r[2] and not r[2].startswith('TC_')] + \
           [47 + i for i, r in enumerate(blockB) if r[2] and not r[2].startswith('TC_')] + [72]
print('section rows', sec_rows)
print('A', [r[2][:12] for r in blockA])
print('B', [r[2][:12] for r in blockB])
