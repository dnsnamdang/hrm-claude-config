# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Danh sách loại phiếu hạch toán" với checklist của tester (06/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../benefit-rates/gen_checklist.py (06/11/2026).
SRS màn này (màn DANH MỤC CHỈ XEM) có 4 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm và lọc · 2.3 Tùy chỉnh cột · 2.4 Xuất Excel (UC).
Màn KHÔNG có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Lịch sử, Xem chi tiết, Import, Cài đặt bộ lọc (bộ lọc gọn 2 ô) → các dòng đó N/A.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from checklist_doi_chieu import write  # noqa: E402
from gen_testcase import CK  # noqa: E402

CHECKLIST_MOI = os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets', 'CHECKLIST_TC_SRS.xlsx')
CHECKLIST_JSON = os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia', 'checklist_mau_tai_lieu.json')


def _doc_checklist_moi(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    out = {}
    for name in ('Testcase', 'SRS'):
        rows, nhom, phan = [], None, None
        for r in wb[name].iter_rows(min_row=2, values_only=True):
            if len(r) < 4 or not str(r[3] or '').strip():
                continue
            nhom = r[1] or nhom
            phan = r[2] or phan
            rows.append((nhom, phan, r[3]))
        out[name] = rows
    return out


def _assert_checklist_moi():
    import io
    import json
    moi = _doc_checklist_moi(CHECKLIST_MOI)
    cu = json.load(io.open(CHECKLIST_JSON, encoding='utf-8'))
    for name in ('Testcase', 'SRS'):
        a = moi[name]
        b = [(it['nhom'], it['phan'], it['noi_dung']) for it in cu[name]]
        lech = [i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y]
        assert len(a) == len(b) and not lech, '%s: checklist mới khác bản JSON, lệch ở stt %s' % (name, lech[:20])
        print('Checklist mới khớp bản JSON: %s %d dòng' % (name, len(a)))


NA_ADD = 'N/A: màn chỉ xem, không có chức năng Thêm mới (hệ thống cũ cũng đã tắt nút Thêm mới)'
NA_EDIT = 'N/A: màn chỉ xem, không có chức năng Chỉnh sửa'
NA_DEL = 'N/A: màn chỉ xem, không có chức năng Xóa'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (danh mục không có trạng thái)'
NA_HIST = 'N/A: màn không có Lịch sử thay đổi (không có thao tác ghi dữ liệu)'
NA_VIEW = 'N/A: màn không có Xem chi tiết (mọi thông tin đã hiện đủ trên dòng danh sách)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel (hệ thống cũ cũng không có)'
NA_APPROVE = 'N/A: màn danh mục không có Duyệt / Không duyệt'
NA_RB = 'N/A: danh mục cố định, không có thao tác tạo / sửa / khóa / xóa / import nên không phát sinh đồng bộ sang màn khác'

NOTE = {
    7: 'màn không có trạng thái — kiểm không có cột / ô lọc Trạng thái',
    21: 'giảm dần theo Loại phiếu và theo Phân loại',
    29: 'tìm không phân biệt dấu theo cách so sánh chữ của cơ sở dữ liệu',
    31: 'ký tự % và _ được tìm đúng nghĩa đen',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    36: 'bộ lọc gọn: chỉ ô tìm nhanh + ô Phân loại',
    45: 'lệch: màn không ghi nhớ bộ lọc khi rời màn (không có trang con) — đúng theo code',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    47: 'tab mới bộ lọc trống',
    48: 'bộ lọc không ghi nhớ nên tài khoản khác luôn thấy trống',
    222: 'lệch: danh sách rỗng KHÔNG tạo file, báo "Không có dữ liệu để xuất" — đúng theo code',
    283: 'loại phiếu đúng Phân loại (cấp cha)',
    287: 'màn không gắn quyền — ai đăng nhập cũng xem được',
    293: 'màn chỉ có Xuất Excel, không có Import',
    295: 'màn không gắn quyền nên không có nút bị ẩn theo quyền',
    296: 'không có quyền để thiếu — kiểm mở link vẫn xem đủ',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm qua mở link',
    298: 'không có quyền — kiểm đổi công ty giữa thao tác',
    299: 'không giới hạn phạm vi — mọi người thấy 105 dòng',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
TC_MAP[8] = ('N/A: danh mục cố định 105 loại phiếu, không có Xóa nên danh sách không thể rỗng khi chưa lọc '
             '(trạng thái rỗng kiểm ở dòng 9)')
TC_MAP[22] = 'N/A: màn không có cột Ngày tạo / Ngày cập nhật (danh mục không lưu ngày) — sắp xếp kiểm ở dòng 20, 21'
for _stt in range(49, 103):
    TC_MAP[_stt] = NA_ADD
for _stt in range(103, 130):
    TC_MAP[_stt] = NA_EDIT
for _stt in range(130, 142):
    TC_MAP[_stt] = NA_DEL
for _stt in range(142, 162):
    TC_MAP[_stt] = NA_LOCK
for _stt in range(162, 186):
    TC_MAP[_stt] = NA_HIST
for _stt in range(186, 198):
    TC_MAP[_stt] = NA_VIEW
for _stt in range(231, 268):
    TC_MAP[_stt] = NA_IMPORT
for _stt in list(range(268, 283)) + [284]:
    TC_MAP[_stt] = NA_RB
TC_MAP[288] = NA_VIEW
TC_MAP[289] = NA_ADD
TC_MAP[290] = NA_EDIT
TC_MAP[291] = NA_DEL
TC_MAP[292] = NA_LOCK
TC_MAP[294] = NA_HIST
for _stt in range(300, 325):
    TC_MAP[_stt] = NA_APPROVE
_miss = [s for s in range(1, 325) if s not in TC_MAP]
assert not _miss, 'Thiếu dòng checklist Testcase: %s' % _miss

NA_S_ADD = 'N/A: màn chỉ xem, không có Thêm mới (ghi rõ ở Phần 1 Phạm vi chức năng và dòng cuối ma trận Phần 2)'
NA_S_EDIT = 'N/A: màn chỉ xem, không có Chỉnh sửa (Phần 1 Phạm vi chức năng)'
NA_S_DEL = 'N/A: màn chỉ xem, không có Xóa (Phần 1 Phạm vi chức năng)'
NA_S_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 1 Phạm vi chức năng, Thuật ngữ "Trạng thái bản ghi")'
NA_S_HIST = 'N/A: màn không có Lịch sử thay đổi (Phần 1 Phạm vi chức năng; Phần 4 — BR-07)'
NA_S_IMPORT = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'
NA_S_VIEW = 'N/A: màn không có Xem chi tiết (Phần 1 Phạm vi chức năng)'
SRS_INTRO = '2.1.1; 2.2.1; 2.3.1; 2.4.2'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1 (Thuật ngữ — màn không có trạng thái)',
    7: 'Phần 1 (Thuật ngữ Phân loại, Hạch toán riêng, PXH / PNH / PT / PC)', 8: 'Phần 1 (Thuật ngữ Cấu trúc phân cấp)',
    9: 'Phần 2 (màn không gắn quyền riêng)', 10: 'Phần 2', 11: 'Phần 2 (không giới hạn phạm vi)', 12: 'Phần 2',
    13: 'Phần 2 (không có Thêm / Sửa / Xóa / Khóa — dòng cuối ma trận)', 14: 'Phần 2 (Xuất Excel; không có Import, Lịch sử)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3 sơ đồ tổng quan; 2.4.1 (Use Case chỉ vẽ cho chức năng thao tác Xuất Excel — 3 chức năng còn lại chỉ xem)',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO, 22: SRS_INTRO,
    23: SRS_INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.2.2; 2.3.2; 2.4.3', 25: '2.1.2; 2.2.2; 2.3.2; 2.4.3 (ảnh menu, sắp xếp, lọc, rỗng, 2 cửa sổ)',
    26: '2.1.3; 2.2.3; 2.3.3; 2.4.4', 27: '2.1.3; 2.2.3; 2.3.3; 2.4.4', 28: '2.1.3; 2.2.3; 2.3.3; 2.4.4',
    29: '2.1.4; 2.2.4; 2.3.4; 2.4.5', 30: '2.1.4; 2.2.4; 2.3.4; 2.4.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1 (Yêu cầu đặc biệt); 2.1.3', 34: '2.1.3 (không có hành động từng dòng)',
    35: '2.1.1; 2.1.4', 36: '2.1.3', 37: '2.1.3', 38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1; 2.2.3', 50: '2.2.3', 51: '2.2.4',
    120: '2.4.2; 2.4.3', 121: '2.4.4', 122: '2.4.2; 2.4.4', 123: '2.4.4', 124: '2.4.4; 2.4.5',
    125: '2.4.2', 126: '2.4.2 (lệch: rỗng không tạo file — đúng theo code)', 127: '2.4.2; 2.4.4', 128: '2.4.4', 129: '2.4.5',
    139: '2.3.1; 2.3.2', 140: '2.3.3', 141: '2.3.1; 2.3.3', 142: '2.3.3; 2.3.4', 143: '2.3.1; 2.3.4', 144: '2.3.1',
    145: '2.3.1', 146: '2.3.4',
    147: 'N/A: màn không nhập liệu nên không có quy tắc duy nhất (danh mục cố định — Phần 4 BR-02)',
    148: 'N/A: màn không nhập liệu (chỉ chuẩn hóa từ khóa tìm kiếm — Phần 4 BR-06)',
    149: 'N/A: không có Khóa và không nhập liệu nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-03 (Phân loại > Loại phiếu); Phần 1 Thuật ngữ', 151: NA_S_DEL, 152: NA_S_LOCK,
    153: 'Phần 4 — BR-09; Phần 5', 154: 'Phần 4 — BR-07', 155: 'Phần 4 — BR-01 đến BR-09',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5',
    160: 'Phần 5 (danh mục không có thao tác ghi nên không ảnh hưởng ngược)',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'N/A: màn không có Xóa (Phần 4 — BR-02)', 163: 'Phần 4 — BR-03; Phần 1 Thuật ngữ Cấu trúc phân cấp',
}
for _stt in range(52, 63):
    SRS_MAP[_stt] = NA_S_ADD
for _stt in range(63, 74):
    SRS_MAP[_stt] = NA_S_EDIT
for _stt in range(74, 83):
    SRS_MAP[_stt] = NA_S_DEL
for _stt in range(83, 94):
    SRS_MAP[_stt] = NA_S_LOCK
for _stt in range(94, 102):
    SRS_MAP[_stt] = NA_S_HIST
for _stt in range(102, 120):
    SRS_MAP[_stt] = NA_S_IMPORT
for _stt in range(130, 139):
    SRS_MAP[_stt] = NA_S_VIEW
_miss = [s for s in range(1, 164) if s not in SRS_MAP]
assert not _miss, 'Thiếu dòng checklist SRS: %s' % _miss

if __name__ == '__main__':
    _assert_checklist_moi()
    write(HERE, TC_MAP, SRS_MAP)
    tc_na = sum(1 for v in TC_MAP.values() if v.startswith('N/A'))
    srs_na = sum(1 for v in SRS_MAP.values() if v.startswith('N/A'))
    print('Testcase: %d có TC / %d N/A; SRS: %d có mục / %d N/A' % (len(TC_MAP) - tc_na, tc_na, len(SRS_MAP) - srs_na, srs_na))
