# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Phiếu chờ giao việc" với checklist của tester (12/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../bien-ban-ban-giao-nghiem-thu/gen_checklist.py. SRS màn này có 12 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Cài đặt bộ
lọc · 2.4 Tùy chỉnh cột · 2.5 Tạo phiếu giao việc (UC) · 2.6 Từ chối tiếp nhận (UC) · 2.7 Đóng hợp đồng (UC) · 2.8 Hủy duyệt (UC) ·
2.9 Mở chức năng ERP · 2.10 Xem chi tiết chứng từ nguồn · 2.11 In phiếu yêu cầu lắp đặt (UC) · 2.12 Xuất Excel (UC).
Mục có UC: .1 Biểu đồ · .2 Giới thiệu · .3 Layout · .4 Giao diện · .5 Event; không UC: .1 Giới thiệu · .2 Layout · .3 Giao diện · .4 Event.
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


HQ = 'màn hàng đợi chỉ xem: chứng từ được lập / sửa ở màn nguồn'
NA_CREATE = 'N/A: %s, không có Thêm mới (Tạo phiếu giao việc mở màn Phiếu giao việc — TC_09.001, TC_09.002)' % HQ
NA_EDIT = 'N/A: %s, không có Chỉnh sửa' % HQ
NA_DEL = 'N/A: %s, không có Xóa (Đóng / Hủy duyệt hợp đồng ở nhóm IV)' % HQ
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa'
NA_HIS = ('N/A: màn không có Lịch sử thay đổi riêng — Từ chối tiếp nhận / Đóng / Hủy duyệt ghi vào lịch sử của hợp đồng ở màn Hợp '
          'đồng dịch vụ (TC_03.009, TC_04.004, TC_04.009)')
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_APPROVE = 'N/A: màn không có Duyệt phiếu (chứng từ đã duyệt ở màn nguồn trước khi vào hàng đợi)'

NOTE = {
    5: 'màn không có cột ẩn mặc định',
    8: 'thẻ rỗng do phạm vi',
    17: 'ô chọn lọc ngay, ô chữ khi bấm Tìm kiếm',
    29: 'mã phiếu không có dấu',
    31: 'lệch: ký tự % và _ là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn ký tự — đúng theo code',
    37: 'lệch: ô Trạng thái liệt kê đủ trạng thái nhưng chỉ trạng thái của thẻ ra dữ liệu — đúng theo code',
    45: 'bộ lọc nhớ 10 phút trên trình duyệt, riêng từng thẻ, kể cả khi sang màn khác',
    46: 'F5 giữ thẻ và bộ lọc',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản — đúng theo code',
    49: 'Tạo phiếu giao việc mở màn khác',
    186: 'chi tiết là trang của màn nguồn, không phải popup',
    196: 'chi tiết là trang: "đóng" là nút Quay lại',
    222: 'lệch: xuất rỗng vẫn ra file chỉ có tên cột và báo thành công — đúng theo code',
    268: 'tương ứng: hợp đồng có PL giảm chờ duyệt thì chặn tạo phiếu giao việc',
    269: 'tương ứng: thẻ Lắp đặt / Giao việc khác không xét quyền Tạo',
    296: 'mở đường dẫn lạ / màn Tạo khi thiếu quyền',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm từ chối khi bị gỡ quyền',
    299: 'mức Công ty không được màn dùng — đúng theo code',
    313: 'nút Từ chối tiếp nhận xử lý (thẻ Hợp đồng, PL bổ sung)',
    317: 'không giới hạn độ dài lý do',
    324: 'phụ lục bổ sung không ghi lịch sử — đúng theo code',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in range(50, 103):
    TC_MAP.setdefault(_stt, NA_CREATE)
for _stt in range(103, 130):
    TC_MAP.setdefault(_stt, NA_EDIT)
for _stt in range(130, 142):
    TC_MAP.setdefault(_stt, NA_DEL)
for _stt in list(range(142, 162)) + [271, 273, 276, 277, 292]:
    TC_MAP.setdefault(_stt, NA_LOCK)
for _stt in list(range(162, 186)) + [294]:
    TC_MAP.setdefault(_stt, NA_HIS)
for _stt in list(range(231, 268)) + [275]:
    TC_MAP.setdefault(_stt, NA_IMPORT)
for _stt in range(300, 313):
    TC_MAP.setdefault(_stt, NA_APPROVE)
TC_MAP.setdefault(194, 'N/A: chứng từ trong hàng đợi không có trạng thái Khóa')
TC_MAP.setdefault(270, NA_DEL)
TC_MAP.setdefault(272, 'N/A: màn không sửa chứng từ; mã chứng từ do màn nguồn sinh, không đổi')
TC_MAP.setdefault(279, 'N/A: màn không sửa chứng từ; mã chứng từ do màn nguồn sinh, không đổi')
TC_MAP.setdefault(280, 'TC_04.004, TC_04.009 (chứng từ Đóng / Không duyệt rời hàng đợi — màn không xóa)')
TC_MAP.setdefault(290, NA_EDIT)
TC_MAP.setdefault(291, NA_DEL)

INTRO = '2.1.1; 2.2.1; 2.3.1; 2.4.1; 2.5.2; 2.6.2; 2.7.2; 2.8.2; 2.9.1; 2.10.1; 2.11.2; 2.12.2'
UI = '2.1.3; 2.2.3; 2.3.3; 2.4.3; 2.5.4; 2.6.4; 2.7.4; 2.8.4; 2.9.3; 2.10.3; 2.11.4; 2.12.4'
EV = '2.1.4; 2.2.4; 2.3.4; 2.4.4; 2.5.5; 2.6.5; 2.7.5; 2.8.5; 2.9.4; 2.10.4; 2.11.5; 2.12.5'
NA_S_CREATE = 'N/A: màn không có Thêm mới (Phần 1 Phạm vi chức năng); Tạo phiếu giao việc chỉ mở màn khác — 2.5'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Thêm / Sửa / Xóa / Khóa — ghi dòng cuối ma trận)', 14: 'Phần 2 (không có Import, Lịch sử riêng)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3 sơ đồ tổng quan; 2.5.1; 2.6.1; 2.7.1; 2.8.1; 2.11.1; 2.12.1',
    18: INTRO, 19: INTRO, 20: INTRO, 21: INTRO, 22: INTRO, 23: INTRO + ' (đoạn "Quy tắc chung" có liên kết)',
    24: '2.1.2 (lối vào duy nhất + 5 thẻ); 2.5.3; 2.6.3', 25: '2.1.2 (5 thẻ, trạng thái rỗng); 2.6.3 (lỗi lý do); 2.11.3',
    26: UI, 27: UI, 28: UI, 29: EV, 30: EV,
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1 (Yêu cầu đặc biệt); 2.1.3; 2.4.3', 34: '2.1.3', 35: '2.1.1; 2.1.3; 2.1.4',
    36: '2.1.3', 37: '2.1.3', 38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1 (Yêu cầu đặc biệt)', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3',
    45: '2.2.3', 46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; 2.5.4 (điều kiện hiện nút Tạo phiếu giao việc, mở màn Tạo)',
    55: 'Phần 4 — BR-12 (màn không tạo bản ghi nên không có quy tắc trùng)',
    83: 'Phần 1 Thuật ngữ (trạng thái của từng thẻ); Phần 4 — BR-02 (không có Khóa / Mở khóa)',
    94: 'Phần 4 — BR-11 (lịch sử thao tác ghi ở màn Hợp đồng dịch vụ)',
    120: '2.12.2; 2.12.3', 121: '2.12.4', 122: '2.12.2; 2.12.4', 123: '2.12.4', 124: '2.12.4; 2.12.5', 125: '2.12.2',
    126: '2.12.2 (rỗng vẫn ra file chỉ có tên cột)', 127: '2.12.2; 2.12.4', 128: '2.12.4', 129: '2.12.5',
    130: '2.10.1', 131: '2.10.2', 132: '2.10.3', 133: '2.10.3', 134: 'N/A: chứng từ trong hàng đợi không có trạng thái Khóa',
    135: '2.10.3 (khối Lịch sử thuộc màn nguồn)', 136: 'N/A: bộ lọc lịch sử thuộc màn nguồn, không đặc tả ở màn này',
    137: '2.10.1; 2.10.4', 138: '2.10.4',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-12', 148: 'Phần 4 — BR-12', 149: 'N/A: không có Khóa nên không có trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-03; Phần 1 Thuật ngữ (Cấu trúc phân cấp)',
    151: 'Phần 4 — BR-07, BR-08 (màn không xóa; điều kiện Đóng / Hủy duyệt)', 152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-10; Phần 5', 154: 'Phần 4 — BR-11', 155: 'Phần 4 — BR-01 đến BR-12',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5 (mã, khách hàng lấy theo chứng từ nguồn)',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5 (dòng 9: chứng từ phía sau chặn Đóng / Hủy duyệt); Phần 4 — BR-07',
    163: 'Phần 5; Phần 4 — BR-03',
}
for _stt in list(range(53, 55)) + list(range(56, 63)):
    SRS_MAP[_stt] = NA_S_CREATE
for _stt in range(63, 74):
    SRS_MAP[_stt] = 'N/A: màn không có Chỉnh sửa (Phần 1 Phạm vi chức năng)'
for _stt in range(74, 83):
    SRS_MAP[_stt] = 'N/A: màn không có Xóa (Phần 1 Phạm vi chức năng); Đóng / Hủy duyệt hợp đồng ở 2.7, 2.8'
for _stt in range(84, 94):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 1 Phạm vi chức năng)'
for _stt in range(95, 102):
    SRS_MAP[_stt] = 'N/A: màn không có Lịch sử thay đổi riêng (Phần 1 Phạm vi chức năng; Phần 4 — BR-11)'
for _stt in range(102, 120):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Import Excel (Phần 1 Phạm vi chức năng)'

_thieu = [i for i in range(1, 325) if i not in TC_MAP]
assert not _thieu, 'Checklist Testcase còn thiếu stt: %s' % _thieu
_thieu = [i for i in range(1, 164) if i not in SRS_MAP]
assert not _thieu, 'Checklist SRS còn thiếu stt: %s' % _thieu

if __name__ == '__main__':
    _assert_checklist_moi()
    write(HERE, TC_MAP, SRS_MAP)
    tc_na = sum(1 for v in TC_MAP.values() if v.startswith('N/A'))
    srs_na = sum(1 for v in SRS_MAP.values() if v.startswith('N/A'))
    print('Testcase: %d có TC / %d N/A; SRS: %d có mục / %d N/A' % (len(TC_MAP) - tc_na, tc_na, len(SRS_MAP) - srs_na, srs_na))
