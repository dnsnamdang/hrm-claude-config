# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Phiếu xuất hàng mượn" với checklist của tester (05/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../finance-bill-adjust-dept/gen_checklist.py. SRS màn này có 10 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Cài đặt bộ lọc ·
2.4 Tùy chỉnh cột · 2.5 Lập phiếu (UC) · 2.6 Chọn phiếu yêu cầu (UC) · 2.7 Xem chi tiết (UC) · 2.8 In (UC) · 2.9 Xuất Excel (UC) ·
2.10 Lịch sử.
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


NA_DRAFT = 'N/A: màn không có Lưu nháp — lưu là ghi ngay, phiếu sinh ra ở trạng thái Đã duyệt'
NA_EDIT = 'N/A: màn không có chức năng Chỉnh sửa (không có nút / màn Sửa; phiếu Đã duyệt không đổi về sau)'
NA_DEL = 'N/A: màn không có chức năng Xóa'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (phiếu chỉ có trạng thái Đã duyệt)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_REJECT = ('N/A: màn không có chức năng Không duyệt — Từ chối phiếu yêu cầu thực hiện ở màn Yêu cầu xuất hàng mượn (đã có tài '
             'liệu riêng)')

NOTE = {
    29: 'so khớp có dấu / không dấu theo cách so sánh chữ của cơ sở dữ liệu — chưa xác minh trên dev',
    31: 'lệch: ký tự % và _ được hiểu là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    45: 'bộ lọc chỉ nhớ 10 phút khi đi vào màn chi tiết / lập phiếu của chính màn',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản',
    54: 'màn Lập là trang: nút Lưu và duyệt / Lưu và tiếp tục / Quay lại',
    67: 'phiếu không có trường nhập duy nhất; một phiếu yêu cầu chỉ duyệt 1 lần',
    76: 'màn Lập là trang, không phải popup — kiểm form trắng sau Lưu và tiếp tục',
    86: 'màn không có "Lưu và gửi duyệt": nút tương ứng là Lưu và duyệt', 87: 'nút tương ứng: Lưu và duyệt',
    88: 'nút tương ứng: Lưu và duyệt', 89: 'nút tương ứng: Lưu và duyệt', 90: 'màn là trang: Lưu và tiếp tục ở lại màn Lập',
    91: 'nút tương ứng: Lưu và tiếp tục', 92: 'màn là trang: sau Lưu và duyệt chuyển về danh sách',
    95: 'màn là trang, không có nút X — kiểm rời màn bằng menu / Quay lại',
    186: 'màn chi tiết là trang, không phải popup', 194: 'màn không có trạng thái Khóa; phiếu luôn Đã duyệt (chỉ xem)',
    196: 'màn chi tiết là trang: "đóng" là nút Quay lại',
    183: 'phiếu không sửa được; một lần duyệt đổi nhiều thông tin của phiếu yêu cầu chỉ ghi 1 mốc',
    222: 'danh sách rỗng vẫn ra file có tiêu đề, tên cột, khối ký — đúng theo code',
    272: 'phiếu không sửa được — kiểm đổi tên hàng ở danh mục không làm đổi phiếu',
    278: 'tên hàng lưu cố định lúc lập', 279: 'mã phiếu tự sinh, không sửa được — kiểm liên kết với phiếu yêu cầu',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm máy chủ chặn qua thao tác của tài khoản vừa bị gỡ quyền',
    300: 'màn không có nút "Duyệt" riêng: Lưu và duyệt chính là duyệt phiếu yêu cầu',
    301: 'lệch: không có cửa sổ xác nhận duyệt — Lưu và duyệt ghi ngay, đúng theo code',
    308: 'thông báo gửi người lập phiếu yêu cầu',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in range(79, 86):
    TC_MAP[_stt] = NA_DRAFT
for _stt in list(range(103, 130)) + [177, 178, 290]:
    TC_MAP[_stt] = NA_EDIT
for _stt in list(range(130, 142)) + [270, 280, 291]:
    TC_MAP[_stt] = NA_DEL
for _stt in list(range(142, 162)) + [179, 180, 271, 273, 276, 277, 292]:
    TC_MAP[_stt] = NA_LOCK
for _stt in list(range(231, 268)) + [181, 275]:
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(313, 325):
    TC_MAP[_stt] = NA_REJECT

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.6.2; 2.7.2; 2.10.1'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2 (không có quyền xem theo cấp — ghi rõ ở mục Danh sách quyền)', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Sửa / Xóa / Khóa — ghi rõ dòng cuối ma trận)', 14: 'Phần 2 (không có Import)', 15: 'Phần 2',
    16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.6.1; 2.7.1; 2.8.1; 2.9.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.4.1; 2.5.2; 2.8.2; 2.9.2',
    23: SRS_INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.6.3', 25: '2.5.3; 2.6.3; 2.8.3; 2.10.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.1.4; 2.5.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1; 2.2.3', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; 2.6.2', 53: '2.5.4; 2.6.4', 54: '2.5.4', 55: '2.5.2; Phần 4 — BR-06', 56: '2.5.4; 2.5.5', 57: '2.5.5',
    58: '2.5.2; 2.5.5', 59: '2.5.2 (màn Lập là trang: không có (x) / click ngoài — ghi rõ cách rời màn); 2.6.2',
    60: '2.5.2; 2.5.5', 61: '2.5.2; 2.5.5', 62: '2.5.5',
    83: 'Phần 1; Phần 4 — BR-04 (không có Khóa / Mở khóa; trạng thái phiếu mô tả ở Thuật ngữ)',
    94: '2.10.1; 2.10.2', 95: '2.10.3', 96: '2.10.3', 97: '2.10.1; 2.10.3', 98: '2.10.1; 2.10.3', 99: '2.10.1',
    100: '2.10.1', 101: '2.10.4',
    120: '2.9.2; 2.9.3', 121: '2.9.4', 122: '2.9.2; 2.9.4', 123: '2.9.4', 124: '2.9.4; 2.9.5', 125: '2.9.2', 126: '2.9.2',
    127: '2.9.2; 2.9.4', 128: '2.9.4', 129: '2.9.5',
    130: '2.7.2', 131: '2.7.3', 132: '2.7.4', 133: '2.7.2; 2.7.4',
    134: '2.7.2 (không có Khóa; phiếu Đã duyệt chỉ xem, chân màn chỉ In, Quay lại)',
    135: '2.7.4; 2.10.3', 136: '2.10.3', 137: '2.7.2; 2.7.5', 138: '2.7.5',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-06', 148: 'Phần 4 — BR-07',
    149: 'N/A: không có Khóa và không có trường nhập duy nhất nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-08', 151: 'Phần 4 — BR-04 (màn không có Xóa)',
    152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-12; Phần 5', 154: 'Phần 4 — BR-13', 155: 'Phần 4 — BR-01 đến BR-13',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5 (phiếu không sửa được sau khi lập)',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5 (màn không có Xóa — phiếu đã lập không gỡ khỏi các màn tham chiếu)', 163: 'Phần 5; Phần 4 — BR-08',
}
for _stt in range(63, 74):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Chỉnh sửa (ghi rõ ở Phần 1 Phạm vi chức năng)'
for _stt in range(74, 83):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Xóa (ghi rõ ở Phần 1 Phạm vi chức năng)'
for _stt in range(84, 94):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
for _stt in range(102, 120):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'

if __name__ == '__main__':
    _assert_checklist_moi()
    write(HERE, TC_MAP, SRS_MAP)
    tc_na = sum(1 for v in TC_MAP.values() if v.startswith('N/A'))
    srs_na = sum(1 for v in SRS_MAP.values() if v.startswith('N/A'))
    print('Testcase: %d có TC / %d N/A; SRS: %d có mục / %d N/A' % (len(TC_MAP) - tc_na, tc_na, len(SRS_MAP) - srs_na, srs_na))
