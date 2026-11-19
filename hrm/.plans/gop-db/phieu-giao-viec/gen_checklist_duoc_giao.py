# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Phiếu giao việc được giao" với checklist của tester (18/11/2026).

Chạy: python gen_checklist_duoc_giao.py -> "Đối chiếu checklist - Phiếu giao việc được giao.xlsx"
(chạy sau gen_testcase_duoc_giao.py và gen_srs_duoc_giao.py).
Hàm ghi dùng chung checklist_doi_chieu.write() luôn đặt tên "Đối chiếu checklist.xlsx" trong thư mục truyền vào → ghi vào thư mục tạm
rồi chuyển sang tên riêng (thư mục này dùng chung với bộ "Phiếu giao việc" sau này). Không sửa thư viện chung.
Khuôn: ../phieu-cho-giao-viec/gen_checklist.py. SRS màn này có 11 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Cài đặt bộ lọc ·
2.4 Tùy chỉnh cột · 2.5 Xem chi tiết · 2.6 Nhập kết quả (UC) · 2.7 Xem phiếu nhập kết quả · 2.8 Xóa (UC) · 2.9 Lịch sử ·
2.10 In danh sách (UC) · 2.11 Xuất Excel (UC).
Mục có UC: .1 Biểu đồ · .2 Giới thiệu · .3 Layout · .4 Giao diện · .5 Event; không UC: .1 Giới thiệu · .2 Layout · .3 Giao diện · .4 Event.
"""
import os
import shutil
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from checklist_doi_chieu import write  # noqa: E402
from gen_testcase_duoc_giao import CK, OUT as TC_FILE  # noqa: E402

SRS_FILE = os.path.join(HERE, 'SRS - Phiếu giao việc được giao.docx')
OUT = os.path.join(HERE, 'Đối chiếu checklist - Phiếu giao việc được giao.xlsx')

NA_CREATE = ('N/A: màn không có Thêm mới — phiếu giao việc lập từ màn Phiếu chờ giao việc; nút Nhập kết quả mở màn khác (TC_09.001, '
             'TC_09.002)')
NA_EDIT = 'N/A: màn không có Chỉnh sửa (giữ như hệ thống ERP — không có lối vào Sửa)'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_APPROVE = 'N/A: màn không có Duyệt phiếu (duyệt kết quả thuộc màn Phiếu nhập kết quả)'
NA_REJECT = 'N/A: màn không có Không duyệt phiếu'

NOTE = {
    5: 'màn không có cột ẩn mặc định',
    8: 'không là người thực hiện phiếu nào',
    29: 'số phiếu không có chữ có dấu',
    31: 'lệch: ký tự % và _ là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn ký tự — đúng theo code',
    45: 'lệch: chỉ giữ bộ lọc khi mở chi tiết rồi quay lại; sang màn khác thì mất — đúng theo code',
    46: 'lệch: F5 không giữ bộ lọc nếu chưa mở chi tiết — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản — đúng theo code',
    186: 'chi tiết là trang, không phải popup',
    196: 'chi tiết là trang: "đóng" là nút Quay lại',
    222: 'lệch: xuất rỗng không ra file, báo "Không có dữ liệu để xuất" — đúng theo code',
    268: 'tương ứng: điều kiện hiện Nhập kết quả / Xem phiếu nhập kết quả',
    269: 'tương ứng: mở màn Tạo phiếu nhập kết quả từ phiếu giao việc',
    270: 'xóa phiếu giao việc trả số lượng về chứng từ nguồn',
    280: 'tương ứng: xóa phiếu nhập kết quả / gỡ khỏi phiếu công tác',
    283: 'tương ứng: phiếu chỉ hiện khi phiếu công tác cha đã duyệt',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm bị gỡ người thực hiện giữa chừng',
    299: 'quyền xem theo cấp không mở rộng màn này — đúng theo code',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in range(49, 103):
    TC_MAP.setdefault(_stt, NA_CREATE)
for _stt in range(103, 130):
    TC_MAP.setdefault(_stt, NA_EDIT)
for _stt in list(range(142, 162)) + [179, 180, 194, 271, 273, 276, 277, 292]:
    TC_MAP[_stt] = NA_LOCK
for _stt in [177, 178, 183]:
    TC_MAP[_stt] = NA_EDIT + ' (mốc Xóa phiếu kiểm ở TC_04.006)'
for _stt in [181, 275] + list(range(231, 268)):
    TC_MAP.setdefault(_stt, NA_IMPORT)
for _stt in range(300, 313):
    TC_MAP.setdefault(_stt, NA_APPROVE)
for _stt in range(313, 325):
    TC_MAP.setdefault(_stt, NA_REJECT)
TC_MAP[289] = 'N/A: màn không có Thêm mới — TC_10.007 kiểm không có nút Tạo mới'
TC_MAP[290] = 'N/A: màn không có Chỉnh sửa — TC_10.007 kiểm không có nút Sửa'
TC_MAP.setdefault(272, 'N/A: màn không sửa phiếu; mã phiếu do màn Phiếu chờ giao việc sinh, không đổi')
TC_MAP.setdefault(278, 'N/A: màn không sửa phiếu; tên khách / chứng từ lấy theo nguồn')
TC_MAP.setdefault(279, 'N/A: màn không sửa phiếu; mã phiếu không đổi')

INTRO = '2.1.1; 2.2.1; 2.3.1; 2.4.1; 2.5.1; 2.6.2; 2.7.1; 2.8.2; 2.9.1; 2.10.2; 2.11.2'
UI = '2.1.3; 2.2.3; 2.3.3; 2.4.3; 2.5.3; 2.6.4; 2.7.3; 2.8.4; 2.9.3; 2.10.4; 2.11.4'
EV = '2.1.4; 2.2.4; 2.3.4; 2.4.4; 2.5.4; 2.6.5; 2.7.4; 2.8.5; 2.9.4; 2.10.5; 2.11.5'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Thêm / Sửa / Khóa — ghi dòng cuối ma trận)', 14: 'Phần 2 (không có Import)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3 sơ đồ tổng quan; 2.6.1; 2.8.1; 2.10.1; 2.11.1',
    18: INTRO, 19: INTRO, 20: INTRO, 21: INTRO, 22: INTRO, 23: INTRO + ' (đoạn "Quy tắc chung" có liên kết)',
    24: '2.1.2 (lối vào + phạm vi hiển thị); 2.5.2; 2.6.3', 25: '2.1.2 (trạng thái rỗng); 2.5.2; 2.8.3; 2.9.2',
    26: UI, 27: UI, 28: UI, 29: EV, 30: EV,
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1 (Yêu cầu đặc biệt); 2.1.3; 2.4.3', 34: '2.1.3', 35: '2.1.1; 2.1.3; 2.1.4',
    36: '2.1.3', 37: '2.1.3', 38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1 (Yêu cầu đặc biệt)', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3',
    45: '2.2.3', 46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.6.2; 2.6.4 (điều kiện hiện nút Nhập kết quả, mở màn Tạo phiếu nhập kết quả)',
    55: 'Phần 4 — BR-12 (màn không tạo bản ghi nên không có quy tắc trùng)',
    74: '2.8.2; Phần 4 — BR-05', 75: '2.8.2 (trả số lượng chứng từ nguồn)', 76: '2.8.2; Phần 4 — BR-05 (đã gắn phiếu công tác thì không xóa)',
    77: 'N/A: màn không có trạng thái Khóa', 78: '2.8.4', 79: '2.8.4', 80: '2.8.2; 2.8.4', 81: '2.8.2; 2.8.5', 82: '2.8.5',
    83: 'Phần 1 Thuật ngữ (8 trạng thái); Phần 4 — BR-06 (không có Khóa / Mở khóa)',
    94: '2.9.1; 2.9.2', 95: '2.9.3', 96: '2.9.3', 97: '2.9.3', 98: '2.9.3', 99: '2.9.1', 100: '2.9.1; 2.9.4', 101: '2.9.4',
    120: '2.11.2; 2.11.3', 121: '2.11.4', 122: '2.11.2; 2.11.4', 123: '2.11.4', 124: '2.11.4; 2.11.5', 125: '2.11.2',
    126: '2.11.2 (rỗng không ra file — đúng theo code)', 127: '2.11.2; 2.11.4', 128: '2.11.4', 129: '2.11.5',
    130: '2.5.1', 131: '2.5.2', 132: '2.5.3', 133: '2.5.3', 134: 'N/A: phiếu giao việc không có trạng thái Khóa',
    135: '2.5.3; 2.9.3', 136: '2.9.3', 137: '2.5.1; 2.5.4', 138: '2.5.4',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-12', 148: 'Phần 4 — BR-12', 149: 'N/A: không có Khóa nên không có trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-02; Phần 1 Thuật ngữ (Cấu trúc phân cấp)', 151: 'Phần 4 — BR-05', 152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-02, BR-06; Phần 5', 154: 'Phần 4 — BR-09', 155: 'Phần 4 — BR-01 đến BR-12',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5 (màn không sửa phiếu; chứng từ nguồn quyết định khách, mã)',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5; Phần 4 — BR-05 (đã gắn phiếu công tác thì không xóa)', 163: 'Phần 5; Phần 4 — BR-02',
}
for _stt in list(range(53, 55)) + list(range(56, 63)):
    SRS_MAP[_stt] = 'N/A: màn không có Thêm mới (Phần 1 Phạm vi chức năng); Nhập kết quả chỉ mở màn khác — 2.6'
for _stt in range(63, 74):
    SRS_MAP[_stt] = 'N/A: màn không có Chỉnh sửa (Phần 1 Phạm vi chức năng)'
for _stt in range(84, 94):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 1 Phạm vi chức năng)'
for _stt in range(102, 120):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Import Excel (Phần 1 Phạm vi chức năng)'

_thieu = [i for i in range(1, 325) if i not in TC_MAP]
assert not _thieu, 'Checklist Testcase còn thiếu stt: %s' % _thieu
_thieu = [i for i in range(1, 164) if i not in SRS_MAP]
assert not _thieu, 'Checklist SRS còn thiếu stt: %s' % _thieu

if __name__ == '__main__':
    tmp = tempfile.mkdtemp(prefix='pgvdg_ck_')
    out = write(tmp, TC_MAP, SRS_MAP, testcase=TC_FILE, srs=SRS_FILE)
    shutil.move(out, OUT)
    shutil.rmtree(tmp, ignore_errors=True)
    tc_na = sum(1 for v in TC_MAP.values() if v.startswith('N/A'))
    srs_na = sum(1 for v in SRS_MAP.values() if v.startswith('N/A'))
    print('Testcase: %d có TC / %d N/A; SRS: %d có mục / %d N/A -> %s'
          % (len(TC_MAP) - tc_na, tc_na, len(SRS_MAP) - srs_na, srs_na, OUT))
