# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Biên bản xử lý hàng thừa, thiếu sau kiểm kê" với checklist của tester (06/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../ke-hoach-tong-kiem-ke-hang-hoa/gen_checklist.py.
SRS màn này có 13 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Cài đặt bộ lọc · 2.4 Tùy chỉnh cột · 2.5 Tạo (UC) · 2.6 Lấy dữ liệu, nhập
xử lý (UC) · 2.7 Lưu và gửi duyệt (UC) · 2.8 Sửa (UC) · 2.9 Xem chi tiết · 2.10 Duyệt (UC) · 2.11 In (UC) · 2.12 Xuất Excel (UC) ·
2.13 Lịch sử.
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


NA_DEL = 'N/A: màn không có chức năng Xóa (hệ thống cũ đã tắt nút Xóa biên bản)'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (biên bản chỉ đổi trạng thái theo vòng đời Đang tạo > Chờ duyệt > Đã duyệt)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_REJECT = 'N/A: màn không có chức năng Không duyệt / Từ chối (như hệ thống cũ) — biên bản Chờ duyệt chỉ có Duyệt'

NOTE = {
    29: 'số phiếu không có chữ có dấu — kiểm không lỗi',
    31: 'lệch: ký tự % và _ được hiểu là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản',
    52: 'Lưu và Lưu và gửi duyệt bắt cùng bộ trường',
    54: 'màn Tạo là trang: Lưu / Lưu và gửi duyệt / Lưu và tiếp tục / Quay lại',
    63: 'ô % chỉ nhận số; Lý do nhận mọi ký tự',
    67: 'biên bản không có trường duy nhất: trùng nội dung vẫn lưu được (không chặn lập trùng — đúng theo code)',
    76: 'màn Tạo là trang, không phải popup — kiểm form trắng sau Lưu và tiếp tục',
    79: 'nút tương ứng: Lưu (trạng thái Đang tạo)', 80: 'nút Lưu', 81: 'nút Lưu', 82: 'nút Lưu',
    83: 'Lưu và tiếp tục lưu ở trạng thái Đang tạo', 84: 'trạng thái sau Lưu: Đang tạo', 85: 'màn là trang: sau Lưu về danh sách',
    86: 'nút Lưu và gửi duyệt (Chờ duyệt)', 90: 'màn là trang: sau Lưu và gửi duyệt về danh sách',
    91: 'Lưu và gửi duyệt không có biến thể "tiếp tục"', 92: 'sau Lưu và gửi duyệt về danh sách',
    95: 'màn là trang, không có nút X — kiểm (x) của hộp chưa lưu',
    103: 'màn Sửa là trang, không phải popup',
    126: 'không có Khóa — tương ứng: biên bản không còn Đang tạo không sửa được',
    129: 'biên bản Chờ duyệt / Đã duyệt không sửa được',
    186: 'màn chi tiết là trang, không phải popup', 194: 'không có Khóa — kiểm nút theo trạng thái',
    196: 'màn chi tiết là trang: "đóng" là Quay lại',
    214: 'lệch: chỉ tích sẵn 5/9 trường dù bảng hiện đủ cột — ghi nhận lỗi nhẹ',
    215: 'lệch: trường mặc định 5/9',
    222: 'danh sách rỗng vẫn ra file — đúng theo code',
    276: 'không có Khóa — kiểm nhân viên nghỉ việc không chọn mới được',
    281: 'trạng thái biên bản đổi theo Lưu và gửi duyệt / Duyệt',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm máy chủ chặn khi gỡ quyền giữa thao tác',
    301: 'lệch: không có cửa sổ xác nhận duyệt — đúng theo code (giữ như hệ thống cũ)',
    307: 'bút toán sổ cái hiện ở sổ công nợ nhân viên',
    308: 'thông báo gửi khi Lưu và gửi duyệt (người duyệt cùng công ty); Duyệt không gửi',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in list(range(130, 142)) + [127, 280, 291]:
    TC_MAP[_stt] = NA_DEL
for _stt in list(range(142, 162)) + [179, 180, 271, 273, 277, 292]:
    TC_MAP[_stt] = NA_LOCK
for _stt in list(range(231, 268)) + [181, 275]:
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(313, 325):
    TC_MAP[_stt] = NA_REJECT
_miss = [s for s in range(1, 325) if s not in TC_MAP]
assert not _miss, 'Thiếu dòng checklist Testcase: %s' % _miss

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.6.2; 2.8.2; 2.9.1; 2.13.1'
NA_S_DEL = 'N/A: màn không có chức năng Xóa (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
NA_S_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
NA_S_IMPORT = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2 (bảng Nhóm quyền quyết định phạm vi dữ liệu V1 / V2)', 12: 'Phần 2',
    13: 'Phần 2 (không có Xóa / Khóa — ghi rõ dòng cuối ma trận)', 14: 'Phần 2 (không có Import)', 15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.6.1; 2.7.1; 2.8.1; 2.10.1; 2.11.1; 2.12.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.4.1; 2.5.2; 2.6.2; 2.7.2; 2.8.2; 2.10.2; 2.11.2; 2.12.2; 2.13.1',
    23: SRS_INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.7.3; 2.10.3', 25: '2.1.2; 2.5.3; 2.6.3; 2.9.2; 2.10.3; 2.11.3; 2.13.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.1.4; 2.5.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; Phần 2', 53: '2.5.4; 2.6.4', 54: '2.5.4', 55: '2.5.2; Phần 4 — BR-10', 56: '2.5.4; 2.5.5; 2.6.5',
    57: '2.5.5; 2.7.5', 58: '2.5.2; 2.5.5', 59: '2.5.2 (màn Tạo là trang: không có (x) / click ngoài — ghi rõ cách rời màn)',
    60: '2.5.2; 2.5.5', 61: '2.5.2; 2.5.5', 62: '2.5.5',
    63: '2.8.2; Phần 2', 64: '2.8.2', 65: '2.8.4', 66: '2.8.5', 67: '2.8.2; Phần 4 — BR-10', 68: '2.8.2', 69: '2.8.5',
    70: '2.8.2; 2.8.5', 71: '2.8.2 (không có Khóa; biên bản không còn Đang tạo không sửa được)', 72: '2.8.2; 2.13.1; Phần 4 — BR-16',
    73: '2.8.5',
    83: 'Phần 1 (Thuật ngữ — các trạng thái); Phần 4 — BR-08',
    94: '2.13.1; 2.13.2', 95: '2.13.3', 96: '2.13.3', 97: '2.13.1; 2.13.3', 98: '2.13.3', 99: '2.13.1', 100: '2.13.1',
    101: '2.13.4',
    120: '2.12.2; 2.12.3', 121: '2.12.4', 122: '2.12.2; 2.12.4 (lệch: tích sẵn 5/9 trường)', 123: '2.12.4', 124: '2.12.4; 2.12.5',
    125: '2.12.2', 126: '2.12.2', 127: '2.12.2; 2.12.4', 128: '2.12.4', 129: '2.12.5',
    130: '2.9.1', 131: '2.9.2', 132: '2.9.3', 133: '2.9.1; 2.9.3',
    134: '2.9.1 (không có Khóa; nút theo trạng thái ghi ở 2.9.3)', 135: '2.9.3; 2.13.3', 136: '2.13.3',
    137: '2.9.1; 2.9.4', 138: '2.9.4',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-10', 148: 'Phần 4 — BR-11',
    149: 'N/A: không có Khóa và không có trường nhập duy nhất nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-12', 151: NA_S_DEL, 152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-15; Phần 5', 154: 'Phần 4 — BR-16', 155: 'Phần 4 — BR-01 đến BR-16',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5; Phần 4 — BR-15',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5; Phần 4 — BR-15 (biên bản không xóa được; kho vật lý đã dùng không xóa được)', 163: 'Phần 5; Phần 4 — BR-12',
}
for _stt in range(74, 83):
    SRS_MAP[_stt] = NA_S_DEL
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
