# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Hệ số công nghệ theo nhóm hàng hóa" với checklist của tester (06/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../bien-ban-xu-ly-thua-thieu-kiem-ke/gen_checklist.py.
SRS màn này (màn DANH MỤC) có 10 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Cài đặt bộ lọc · 2.4 Tùy chỉnh cột · 2.5 Thêm mới (UC) ·
2.6 Sửa (UC) · 2.7 Xóa (UC) · 2.8 Xem chi tiết · 2.9 Lịch sử · 2.10 Xuất Excel (UC).
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


NA_DRAFT = 'N/A: màn danh mục không có Lưu nháp / Lưu và gửi duyệt (popup chỉ có Lưu, Lưu và tiếp tục, Đóng)'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (bản ghi không có trạng thái, giữ như hệ thống cũ)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel (hệ thống cũ cũng không có)'
NA_APPROVE = 'N/A: màn danh mục không có Duyệt / Không duyệt'

NOTE = {
    29: 'tìm không phân biệt dấu theo cách so sánh chữ của cơ sở dữ liệu',
    31: 'ký tự % và _ được tìm đúng nghĩa đen',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    45: 'lệch: màn không ghi nhớ bộ lọc khi rời màn (không có trang con) — đúng theo code',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    47: 'tab mới bộ lọc trống',
    48: 'bộ lọc không ghi nhớ nên tài khoản khác luôn thấy trống',
    59: 'màn không có trạng thái — kiểm hệ số có hiệu lực ngay',
    62: 'ô Hệ số tự bỏ ký tự sai ngay khi gõ',
    64: 'không có độ dài tối thiểu (≥ 1 ký tự); Hệ số cho phép 0',
    67: 'trùng tên trong công ty + nhóm đã thuộc loại hệ số khác (kiểm toàn hệ thống)',
    100: 'kiểm lưu bình thường sau thời gian chờ (phiên còn hạn)',
    129: 'sửa hệ số không đổi số đã chép trên phiếu cũ',
    135: 'lệch: không chặn xóa khi hệ số đã dùng ở phiếu (phiếu chỉ chép số) — đúng theo code, user chốt 13/10',
    136: 'dữ liệu con = các nhóm áp dụng, bị xóa kèm',
    141: 'phiếu đã lưu giữ nguyên số hệ số',
    167: 'loại hành động: Tạo mới / Thay đổi thông tin; Xóa ghi nhưng không xem được',
    186: 'xem chi tiết là popup',
    190: 'lệch nhẹ: popup Xem hiện Hệ số "1.5", danh sách "1.50"',
    222: 'lệch: danh sách rỗng KHÔNG tạo file, báo "Không có dữ liệu để xuất" — đúng theo code',
    270: 'lệch: không chặn xóa khi có liên quan — đúng theo code (phiếu chỉ chép số)',
    276: 'không có Khóa hệ số — kiểm nhóm hàng hóa đã khóa không chọn mới được',
    282: 'bộ lọc Người tạo / Người cập nhật của chính màn cập nhật sau khi thêm',
    284: 'nhóm hàng hóa bị khóa vẫn giữ liên kết, hiện kèm ổ khóa',
    287: 'màn không gắn quyền — ai đăng nhập cũng xem được',
    295: 'màn không gắn quyền nên không có nút bị ẩn theo quyền',
    296: 'không có quyền để thiếu — kiểm phạm vi công ty khi mở link',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm máy chủ bó theo công ty khi mở link',
    298: 'không có quyền — kiểm đổi công ty giữa thao tác',
    299: 'phạm vi theo công ty người đăng nhập',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in range(79, 93):
    TC_MAP[_stt] = NA_DRAFT
for _stt in list(range(142, 162)) + [126, 137, 179, 180, 194, 271, 273, 277, 281, 292]:
    TC_MAP[_stt] = NA_LOCK
for _stt in list(range(231, 268)) + [181, 275]:
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(300, 325):
    TC_MAP[_stt] = NA_APPROVE
TC_MAP[279] = 'N/A: màn không có trường mã (bản ghi định danh bằng Loại hệ số; đổi tên nhóm hàng hóa kiểm ở dòng 278)'
_miss = [s for s in range(1, 325) if s not in TC_MAP]
assert not _miss, 'Thiếu dòng checklist Testcase: %s' % _miss

NA_S_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dòng cuối ma trận Phần 2)'
NA_S_IMPORT = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'
SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.6.2; 2.7.2; 2.8.1; 2.9.1; 2.10.2'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1 (Thuật ngữ — màn không có trạng thái)',
    7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2 (màn không gắn quyền riêng)', 10: 'Phần 2', 11: 'Phần 2 (bảng Nhóm quyền quyết định phạm vi dữ liệu — theo công ty)',
    12: 'Phần 2', 13: 'Phần 2 (không có Khóa — ghi rõ dòng cuối ma trận)', 14: 'Phần 2 (không có Import)', 15: 'Phần 2',
    16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.6.1; 2.7.1; 2.10.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.4.1; 2.5.2; 2.6.2; 2.7.2; 2.10.2',
    23: SRS_INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.6.3; 2.7.3; 2.10.3', 25: '2.1.2; 2.5.3; 2.6.3; 2.7.3; 2.8.2; 2.9.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.1.4; 2.5.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.1; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; Phần 2', 53: '2.5.4', 54: '2.5.4', 55: '2.5.2; Phần 4 — BR-02, BR-03', 56: '2.5.4; 2.5.5',
    57: '2.5.2; 2.5.5', 58: '2.5.2; 2.5.5', 59: '2.5.2; 2.5.4', 60: '2.5.2; 2.5.4; 2.5.5', 61: '2.5.2; 2.5.5', 62: '2.5.5',
    63: '2.6.2; Phần 2', 64: '2.6.2', 65: '2.6.2; 2.6.4', 66: '2.6.4; 2.6.5', 67: '2.6.5; Phần 4 — BR-02, BR-03', 68: '2.6.1; 2.6.5',
    69: '2.6.2; 2.6.5', 70: '2.6.2; 2.6.5', 71: '2.6.2 (không có Khóa — Yêu cầu đặc biệt)', 72: '2.6.2; 2.6.5; Phần 4 — BR-09',
    73: '2.6.5',
    74: '2.7.2; Phần 2', 75: '2.7.2; Phần 4 — BR-06, BR-07', 76: '2.7.2; Phần 4 — BR-06, BR-08',
    77: '2.7.2 (không có Khóa)', 78: '2.7.3; 2.7.4', 79: '2.7.4', 80: '2.7.2; 2.7.5', 81: '2.7.2; 2.7.4', 82: '2.7.5',
    94: '2.9.1; 2.9.2', 95: '2.9.3', 96: '2.9.3', 97: '2.9.1; 2.9.3', 98: '2.9.3', 99: '2.9.1; 2.9.3', 100: '2.9.1; 2.9.4',
    101: '2.9.4',
    120: '2.10.2; 2.10.3', 121: '2.10.4', 122: '2.10.2; 2.10.4', 123: '2.10.4', 124: '2.10.4; 2.10.5',
    125: '2.10.2', 126: '2.10.2 (lệch: rỗng không tạo file — đúng theo code)', 127: '2.10.2; 2.10.4', 128: '2.10.4', 129: '2.10.5',
    130: '2.8.1', 131: '2.8.2', 132: '2.8.3', 133: '2.8.1; 2.8.3',
    134: '2.8.3 (không có Khóa; nhóm hàng hóa đã khóa kèm ổ khóa)', 135: '2.8.3; 2.9.3', 136: '2.9.3', 137: '2.8.1; 2.8.4',
    138: '2.8.4',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-02, BR-03', 148: 'Phần 4 — BR-05',
    149: 'N/A: không có Khóa nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-07', 151: 'Phần 4 — BR-06', 152: NA_S_LOCK,
    153: 'Phần 4 — BR-08; Phần 5', 154: 'Phần 4 — BR-09', 155: 'Phần 4 — BR-01 đến BR-10',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5; Phần 4 — BR-08',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 4 — BR-06, BR-08 (không chặn xóa: phiếu chỉ chép số hệ số)', 163: 'Phần 4 — BR-03, BR-07',
}
for _stt in range(83, 94):
    SRS_MAP[_stt] = NA_S_LOCK
for _stt in range(102, 120):
    SRS_MAP[_stt] = NA_S_IMPORT
_miss = [s for s in range(1, 164) if s not in SRS_MAP]
assert not _miss, 'Thiếu dòng checklist SRS: %s' % _miss

if __name__ == '__main__':
    _assert_checklist_moi()
    write(HERE, TC_MAP, SRS_MAP)
    tc_na = sum(1 for v in TC_MAP.values() if v.startswith('N/A'))
    srs_na = sum(1 for v in SRS_MAP.values() if v.startswith('N/A'))
    print('Testcase: %d có TC / %d N/A; SRS: %d có mục / %d N/A' % (len(TC_MAP) - tc_na, tc_na, len(SRS_MAP) - srs_na, srs_na))
