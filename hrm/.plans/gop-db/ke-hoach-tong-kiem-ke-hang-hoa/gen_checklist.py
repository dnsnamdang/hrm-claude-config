# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Kế hoạch tổng kiểm kê hàng hóa" với checklist của tester (05/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../ke-hoach-kiem-ke-theo-hang-hoa/gen_checklist.py (SRS_MAP dời số mục vì màn này không có mục Thêm hàng hóa).
SRS màn này có 13 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Cài đặt bộ lọc · 2.4 Tùy chỉnh cột · 2.5 Tạo (UC) · 2.6 Lưu và duyệt (UC) ·
2.7 Sửa (UC) · 2.8 Xóa (UC) · 2.9 Xem chi tiết · 2.10 Lập phiếu kiểm kê hàng hóa (UC) · 2.11 In (UC) · 2.12 Xuất Excel (UC) · 2.13 Lịch sử.
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



NA_LOCK = ('N/A: màn không có chức năng Khóa / Mở khóa (kế hoạch chỉ đổi trạng thái theo vòng đời Đang tạo > Đã duyệt)')
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_REJECT = 'N/A: màn không có chức năng Không duyệt — Lưu và duyệt chuyển thẳng Đã duyệt, không có người duyệt / từ chối'

NOTE = {
    29: 'so khớp có dấu / không dấu theo cách so sánh chữ của cơ sở dữ liệu — chưa xác minh trên dev',
    31: 'lệch: ký tự % và _ được hiểu là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản',
    52: 'cả 6 ô có dấu *; Lưu nháp chỉ bắt 2 ô ngày, Lưu và duyệt bắt đủ',
    54: 'màn Tạo là trang: nút Lưu nháp / Lưu và duyệt / Lưu và tiếp tục / Quay lại',
    56: 'trường bắt buộc tối thiểu của Lưu nháp = 2 ô ngày',
    63: 'Kho / Công ty thuê kho / Thành phần tham gia là ô chọn; ô nhập tự do duy nhất là Nội dung yêu cầu',
    64: 'Nội dung yêu cầu 255 ký tự', 65: 'Nội dung yêu cầu tối đa 255 ký tự', 66: 'ô Nội dung yêu cầu chặn gõ quá 255 ký tự',
    67: 'kế hoạch không có trường duy nhất: trùng nội dung vẫn lưu được; trùng kho / công ty / phòng ban trong 1 kế hoạch bị chặn',
    68: 'Nội dung yêu cầu', 69: 'Nội dung yêu cầu',
    76: 'màn Tạo là trang, không phải popup — kiểm form trắng sau Lưu và tiếp tục',
    83: 'nút Lưu và tiếp tục lưu ở trạng thái Đang tạo (như Lưu nháp)', 84: 'trạng thái sau Lưu nháp: Đang tạo',
    85: 'màn là trang: sau Lưu nháp về danh sách',
    86: 'nút tương ứng: Lưu và duyệt (trạng thái Đã duyệt)', 87: 'nút tương ứng: Lưu và duyệt', 88: 'nút tương ứng: Lưu và duyệt',
    89: 'nút tương ứng: Lưu và duyệt', 90: 'màn là trang: sau Lưu và duyệt về danh sách',
    91: 'Lưu và duyệt không có biến thể "tiếp tục"', 92: 'sau Lưu và duyệt về danh sách',
    95: 'màn là trang, không có nút X — kiểm rời màn bằng menu / (x) của hộp chưa lưu',
    103: 'màn Sửa là trang, không phải popup', 114: 'chỉ Nội dung yêu cầu là ô nhập tự do', 115: 'chỉ Nội dung yêu cầu là ô nhập tự do',
    126: 'không có Khóa — tương ứng: kế hoạch Đã duyệt không sửa được',
    137: 'không có Khóa — tương ứng: kế hoạch Đã duyệt không xóa được',
    186: 'màn chi tiết là trang, không phải popup', 194: 'không có Khóa — kiểm nút theo trạng thái Đang tạo / Đã duyệt',
    196: 'màn chi tiết là trang: "đóng" là Quay lại',
    222: 'danh sách rỗng vẫn ra file có tiêu đề, tên cột, khối ký — đúng theo code',
    223: 'màn không có xuất Excel 1 kế hoạch (hệ thống cũ không có)',
    276: 'không có Khóa ở màn này — kiểm kho / phòng ban ngừng hoạt động không hiện để chọn mới, kế hoạch Đang tạo không vào popup',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm máy chủ chặn qua thao tác 2 tab',
    300: 'màn không có người duyệt riêng: nhóm Duyệt phiếu tương ứng nút Lưu và duyệt',
    301: 'lệch: không có cửa sổ xác nhận — Lưu và duyệt lưu ngay, đúng theo code (giữ như hệ thống cũ)',
    302: 'Lưu và duyệt', 303: 'Lưu và duyệt bắt đủ 6 trường', 304: 'ngày đến ≥ ngày từ; điều kiện ngày của nút Lập phiếu',
    305: 'trạng thái Đã duyệt', 306: 'Lưu và duyệt',
    307: 'kế hoạch Đã duyệt còn hạn hiện ở popup Chọn kế hoạch của màn Kiểm kê theo hàng hóa',
    308: 'thông báo gửi người có quyền Lập phiếu kiểm kê kho theo hàng hóa cùng công ty',
    310: 'không có hộp xác nhận: hủy = rời màn chưa lưu', 311: 'kế hoạch Đã duyệt không lưu lại được',
    312: 'mốc Thay đổi trạng thái Đang tạo > Đã duyệt',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in list(range(142, 162)) + [179, 180, 271, 273, 277, 292]:
    TC_MAP[_stt] = NA_LOCK
for _stt in list(range(231, 268)) + [181, 275]:
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(313, 325):
    TC_MAP[_stt] = NA_REJECT
_miss = [s for s in range(1, 325) if s not in TC_MAP]
assert not _miss, 'Thiếu dòng checklist Testcase: %s' % _miss

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.7.2; 2.8.2; 2.9.1; 2.13.1'
NA_S_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
NA_S_IMPORT = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2 (bảng Nhóm quyền quyết định phạm vi dữ liệu V1 / V2)', 12: 'Phần 2',
    13: 'Phần 2 (không có Khóa — ghi rõ dòng cuối ma trận)', 14: 'Phần 2 (không có Import)', 15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.6.1; 2.7.1; 2.8.1; 2.10.1; 2.11.1; 2.12.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.4.1; 2.5.2; 2.6.2; 2.7.2; 2.8.2; 2.11.2; 2.12.2; 2.13.1',
    23: SRS_INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.6.3; 2.7.3', 25: '2.1.2; 2.5.3; 2.8.3; 2.9.2; 2.11.3; 2.13.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.1.4; 2.5.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; Phần 2', 53: '2.5.4', 54: '2.5.4', 55: '2.5.2; Phần 4 — BR-06', 56: '2.5.4; 2.5.5',
    57: '2.5.5; 2.6.5', 58: '2.5.2; 2.5.5', 59: '2.5.2 (màn Tạo là trang: không có (x) / click ngoài — ghi rõ cách rời màn)',
    60: '2.5.2; 2.5.5', 61: '2.5.2; 2.5.5', 62: '2.5.5',
    63: '2.7.2; Phần 2', 64: '2.7.2', 65: '2.7.4', 66: '2.7.5', 67: '2.7.2; Phần 4 — BR-06', 68: '2.7.2', 69: '2.7.5',
    70: '2.7.2; 2.7.5', 71: '2.7.2 (không có Khóa; kế hoạch Đã duyệt không sửa được)', 72: '2.7.2; 2.13.1; Phần 4 — BR-13',
    73: '2.7.5',
    74: '2.8.2; 2.8.4', 75: '2.8.2', 76: '2.8.2; Phần 4 — BR-04', 77: '2.8.2 (không có Khóa; kế hoạch Đã duyệt không xóa được)',
    78: '2.8.4', 79: '2.8.4', 80: '2.8.5', 81: '2.8.2; 2.8.5', 82: '2.8.5',
    83: 'Phần 1 (Thuật ngữ — các trạng thái); Phần 4 — BR-05',
    94: '2.13.1; 2.13.2', 95: '2.13.3', 96: '2.13.3', 97: '2.13.1; 2.13.3', 98: '2.13.3', 99: '2.13.1', 100: '2.13.1',
    101: '2.13.4',
    120: '2.12.2; 2.12.3', 121: '2.12.4', 122: '2.12.2; 2.12.4', 123: '2.12.4', 124: '2.12.4; 2.12.5', 125: '2.12.2',
    126: '2.12.2', 127: '2.12.2; 2.12.4', 128: '2.12.4', 129: '2.12.5',
    130: '2.9.1', 131: '2.9.2', 132: '2.9.3', 133: '2.9.1; 2.9.3',
    134: '2.9.1 (không có Khóa; nút theo trạng thái ghi ở 2.9.3)', 135: '2.9.3; 2.13.3', 136: '2.13.3',
    137: '2.9.1; 2.9.4', 138: '2.9.4',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-06', 148: 'Phần 4 — BR-07',
    149: 'N/A: không có Khóa và không có trường nhập duy nhất nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-08', 151: 'Phần 4 — BR-04', 152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-12; Phần 5', 154: 'Phần 4 — BR-13', 155: 'Phần 4 — BR-01 đến BR-13',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5; Phần 4 — BR-01 (kế hoạch không ghi tồn)',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5; Phần 4 — BR-12', 163: 'Phần 5; Phần 4 — BR-08',
}
for _stt in range(84, 94):
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
