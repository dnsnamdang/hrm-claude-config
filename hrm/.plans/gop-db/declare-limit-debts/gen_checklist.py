# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Khai báo hạn mức công nợ KH" với checklist của tester (18/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../benefit-rates/gen_checklist.py.
SRS màn này có 6 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Tùy chỉnh cột · 2.4 Khai báo / chỉnh sửa (UC) · 2.5 Lịch sử ·
2.6 Xuất Excel (UC). Không có Thêm mới (nút), Xóa, Khóa, Xem chi tiết, Import, Cài đặt bộ lọc, Duyệt.
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


NA_ADD = 'N/A: màn không có nút / popup Thêm mới (khai lần đầu = nhập vào dòng trống của khách trên bảng, kiểm ở nhóm Chỉnh sửa)'
NA_CONT = 'N/A: màn không có Lưu và tiếp tục (mỗi khách có 1 nút Lưu trên dòng)'
NA_DRAFT = 'N/A: màn không có Lưu nháp / Lưu và gửi duyệt (chỉ có nút Lưu từng khách)'
NA_DEL = 'N/A: màn không có chức năng Xóa (xoá hạn mức = xoá trắng ô rồi Lưu, kiểm ở TC_03.011)'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (dòng hạn mức không có trạng thái, giữ như hệ thống cũ)'
NA_VIEW = 'N/A: màn không có Xem chi tiết (mọi thông tin hiện trên bảng; hệ thống cũ cũng không có)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel (hệ thống cũ cũng không có)'
NA_APPROVE = 'N/A: màn danh mục không có Duyệt / Không duyệt'

NOTE = {
    28: 'ô tìm nhanh chỉ tìm SĐT / MST / CMND — tìm bằng chữ tên khách thì rỗng',
    29: 'như dòng 28',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    45: 'chuyển sang màn khác thì xoá bộ lọc — đúng theo code',
    46: 'F5 trong 10 phút giữ bộ lọc',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản — đúng theo code',
    51: 'khai lần đầu trên dòng trống — không có popup Thêm mới',
    52: 'như dòng 51', 53: 'như dòng 51', 54: 'nút Lưu từng khách; không có Lưu và tiếp tục / Đóng',
    55: 'khai lần đầu', 59: 'màn không có trạng thái — kiểm báo cáo đọc ngay',
    60: 'lần khai đầu ghi mốc "Thay đổi thông tin", không có mốc Tạo mới',
    63: 'ô số chỉ nhận chữ số', 64: 'không có độ dài tối thiểu; 0 hợp lệ',
    67: 'màn không có trường duy nhất — kiểm lưu được',
    93: 'không có popup — kiểm rời màn khi có / không có khách sửa dở', 94: 'như dòng 93', 95: 'hộp "Thông tin chưa lưu" khi rời màn',
    100: 'kiểm lưu bình thường khi phiên còn hạn; hết phiên thì về đăng nhập',
    102: 'lệch: giữ như hệ thống cũ — người sau lưu có thể xoá dòng công ty khác (user chốt 14/10)',
    103: 'sửa thẳng trên bảng, không có popup', 116: 'không có trường duy nhất',
    124: 'đổi trang / lọc bỏ phần sửa dở, không hỏi — giữ như hệ thống cũ',
    128: 'như dòng 102',
    162: 'cửa sổ lịch sử mở từ cột Hành động',
    167: 'chỉ có mốc "Thay đổi thông tin"',
    176: 'không có mốc Tạo mới — lần khai đầu ghi "Thay đổi thông tin"',
    269: 'khách đã có dòng thì không thêm dòng công ty khác — giữ như hệ thống cũ',
    272: 'đổi tên / mã khách ở danh mục Khách hàng', 279: 'như dòng 272',
    280: 'xoá trắng hạn mức thì báo cáo không còn dòng',
    281: 'Yêu cầu xuất hàng / xuất bán hàng mượn chuyển chờ Trưởng phòng duyệt khi vượt hạn mức',
    285: 'lệch: người chỉ có quyền Quản lý lưu là xoá dòng công ty khác — giữ như hệ thống cũ',
    287: 'màn không chặn quyền xem — ai đăng nhập cũng xem được',
    289: 'khai lần đầu = quyền Quản lý', 293: 'xuất Excel không cần quyền',
    296: 'màn không chặn quyền xem — mở đường dẫn vẫn xem được, không sửa',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm máy chủ từ chối khi quyền vừa bị thu hồi',
    299: 'phạm vi dòng theo quyền + công ty đang làm việc',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
TC_MAP[176] = 'TC_03.006 (%s)' % NOTE[176]
for _stt in (49, 50):
    TC_MAP[_stt] = NA_ADD
for _stt in range(72, 79):
    TC_MAP[_stt] = NA_CONT
for _stt in range(79, 93):
    TC_MAP[_stt] = NA_DRAFT
for _stt in list(range(130, 142)) + [270, 291]:
    TC_MAP[_stt] = NA_DEL
for _stt in list(range(142, 162)) + [126, 179, 180, 271, 273, 276, 277, 284, 292]:
    TC_MAP[_stt] = NA_LOCK
for _stt in list(range(186, 198)) + [288]:
    TC_MAP[_stt] = NA_VIEW
for _stt in list(range(231, 268)) + [181, 275]:
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(300, 325):
    TC_MAP[_stt] = NA_APPROVE
_miss = [s for s in range(1, 325) if s not in TC_MAP]
assert not _miss, 'Thiếu dòng checklist Testcase: %s' % _miss

NA_S_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dòng cuối ma trận Phần 2)'
NA_S_IMPORT = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'
NA_S_DEL = 'N/A: màn không có chức năng Xóa (Phần 1 Phạm vi chức năng; xoá hạn mức = xoá trắng rồi Lưu — Phần 4 BR-09)'
NA_S_VIEW = 'N/A: màn không có Xem chi tiết (Phần 1 Phạm vi chức năng)'
INTRO = '2.1.1; 2.2.1; 2.3.1; 2.4.2; 2.5.1; 2.6.2'
LAYOUT = '2.1.2; 2.2.2; 2.3.2; 2.4.3; 2.5.2; 2.6.3'
UI = '2.1.3; 2.2.3; 2.3.3; 2.4.4; 2.5.3; 2.6.4'
EV = '2.1.4; 2.2.4; 2.3.4; 2.4.5; 2.5.4; 2.6.5'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1 (Thuật ngữ — màn không có trạng thái)',
    7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2 (bảng Nhóm quyền quyết định phạm vi dữ liệu)', 12: 'Phần 2',
    13: 'Phần 2 (không có Thêm / Xóa / Khóa — dòng cuối ma trận)', 14: 'Phần 2 (không có Import)', 15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.4.1; 2.6.1',
    18: INTRO, 19: INTRO, 20: INTRO, 21: INTRO, 22: INTRO,
    23: INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: LAYOUT, 25: LAYOUT + ' (ảnh lỗi dưới ô, hộp chưa lưu, bộ lọc lịch sử)',
    26: UI, 27: UI, 28: UI, 29: EV, 30: EV,
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.3.3', 34: '2.1.3', 35: '2.1.1; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.4.2; Phần 2 (không có nút Thêm mới — khai lần đầu trên dòng trống)', 53: '2.4.4', 54: '2.4.4',
    55: '2.4.2 (Yêu cầu đặc biệt: không có trường duy nhất); Phần 4 — BR-02', 56: '2.4.4; 2.4.5', 57: '2.4.2; 2.4.5',
    58: 'N/A: màn không có Lưu và tiếp tục (Yêu cầu đặc biệt 2.4.2)', 59: '2.4.2 (không có popup — hộp chưa lưu khi rời màn)',
    60: '2.4.2; 2.4.4', 61: '2.4.2; 2.4.5; Phần 4 — BR-07', 62: '2.4.5',
    63: '2.4.2; Phần 2', 64: '2.4.4', 65: '2.4.4; Phần 2; Phần 4 — BR-03', 66: '2.4.4; 2.4.5',
    67: '2.4.2 (không có trường duy nhất — không kiểm trùng)', 68: '2.4.2 (như dòng 67)', 69: '2.4.2; 2.4.5', 70: '2.4.2; 2.4.5',
    71: 'N/A: màn không có Khóa (Phần 1)', 72: '2.4.5; 2.5.3; Phần 4 — BR-07', 73: '2.4.5',
    94: '2.5.1; 2.5.2', 95: '2.5.3', 96: '2.5.3', 97: '2.5.1; 2.5.3', 98: '2.5.3', 99: '2.5.1; 2.5.3', 100: '2.5.1; 2.5.4',
    101: '2.5.4',
    120: '2.6.2; 2.6.4', 121: '2.6.4', 122: '2.6.2; 2.6.4', 123: '2.6.4', 124: '2.6.4; 2.6.5',
    125: '2.6.2', 126: '2.6.2 (lệch: rỗng không tạo file — đúng theo code)', 127: '2.6.2; 2.6.4', 128: '2.6.4', 129: '2.6.5',
    139: '2.3.1; 2.3.2', 140: '2.3.3', 141: '2.3.1; 2.3.3', 142: '2.3.3; 2.3.4', 143: '2.3.1; 2.3.4', 144: '2.3.1',
    145: '2.3.1', 146: '2.3.4',
    147: 'Phần 4 — BR-02, BR-04 (không có trường duy nhất; mỗi khách × công ty tối đa 1 dòng)', 148: 'Phần 4 — BR-05',
    149: 'N/A: không có Khóa nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-02, BR-04', 151: 'Phần 4 — BR-09 (không có Xóa)', 152: NA_S_LOCK,
    153: 'Phần 4 — BR-08; Phần 5', 154: 'Phần 4 — BR-07', 155: 'Phần 4 — BR-01 đến BR-10',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5; Phần 4 — BR-08',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 4 — BR-09; Phần 5 (khách bị xóa ở danh mục Khách hàng thì không còn hiện)', 163: 'Phần 4 — BR-02, BR-04',
}
for _stt in range(74, 83):
    SRS_MAP[_stt] = NA_S_DEL
for _stt in range(83, 94):
    SRS_MAP[_stt] = NA_S_LOCK
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
