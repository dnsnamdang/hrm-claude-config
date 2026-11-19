# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Kiểm kê theo hàng hóa" (phiếu kiểm kê theo hàng hóa) với checklist của tester (06/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../kiem-ke-theo-vi-tri/gen_checklist.py. SRS màn này có 18 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm ·
2.3 Cài đặt bộ lọc · 2.4 Tùy chỉnh cột · 2.5 Tạo (UC) · 2.6 Chọn kế hoạch (UC) · 2.7 Thêm hàng, Làm mới số liệu, ĐVT (UC) ·
2.8 Lưu và gửi (UC) · 2.9 Sửa (UC) · 2.10 Xóa (UC) · 2.11 Xem chi tiết · 2.12 Cập nhật kết quả (UC) · 2.13 Duyệt (UC) ·
2.14 Không duyệt (UC) · 2.15 Xử lý (UC) · 2.16 In (UC) · 2.17 Xuất Excel (UC) · 2.18 Lịch sử.
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


NA_LOCK = ('N/A: màn không có chức năng Khóa / Mở khóa (phiếu chỉ đổi trạng thái theo vòng đời Đang tạo > Đang kiểm > '
           'Chờ KT duyệt > Chờ xử lý > Đang xử lý > Hoàn thành)')
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'

NOTE = {
    29: 'so khớp có dấu / không dấu theo cách so sánh chữ của cơ sở dữ liệu — chưa xác minh trên dev',
    31: 'lệch: ký tự % và _ được hiểu là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt (riêng từng lối vào), không theo tài khoản',
    63: 'ô văn bản tự do duy nhất là Ghi chú (≤ 255)', 67: 'phiếu không có trường duy nhất: trùng nội dung vẫn lưu được (trừ hàng trùng kế hoạch tổng)',
    76: 'màn Tạo là trang, không phải popup — kiểm form trắng sau Lưu và tiếp tục',
    79: 'nút tương ứng là Lưu (trạng thái Đang tạo)', 80: 'nút tương ứng: Lưu; lỗi bắt buộc do máy chủ trả về', 81: 'nút tương ứng: Lưu',
    82: 'nút tương ứng: Lưu', 83: 'nút tương ứng: Lưu và tiếp tục', 84: 'trạng thái sau Lưu: Đang tạo',
    85: 'màn là trang: sau Lưu về danh sách',
    86: 'nút tương ứng: Lưu và gửi (trạng thái Đang kiểm)', 87: 'nút tương ứng: Lưu và gửi',
    88: 'nút tương ứng: Lưu và gửi', 89: 'nút tương ứng: Lưu và gửi', 90: 'màn là trang: sau Lưu và gửi về danh sách',
    91: 'Lưu và gửi không có biến thể "tiếp tục"', 92: 'sau Lưu và gửi về danh sách',
    95: 'màn là trang, không có nút X — kiểm rời màn bằng menu / (x) của hộp chưa lưu',
    103: 'màn Sửa là trang, không phải popup',
    126: 'không có Khóa — tương ứng: phiếu đã gửi không sửa được',
    137: 'không có Khóa — tương ứng: phiếu đã gửi không xóa được',
    141: 'lệch: xóa phiếu KHÔNG trả trạng thái kế hoạch nguồn (giữ như hệ thống cũ, đã chốt 20/10)',
    186: 'màn chi tiết là trang, không phải popup', 194: 'không có Khóa — kiểm nút theo trạng thái Đang tạo / Đang kiểm',
    196: 'màn chi tiết là trang: "đóng" là Quay lại (về đúng lối vào)',
    214: 'nghi lỗi: trường Người duyệt không được tích sẵn dù cột đang hiện ("Đang chọn 10/11 trường") — chưa sửa code',
    222: 'danh sách rỗng vẫn ra file có tiêu đề, tên cột, khối ký — đúng theo code',
    276: 'không có Khóa ở màn này — kiểm kho đã khóa không chọn được, kế hoạch hết kỳ / không Đang kiểm không hiện ở popup',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm máy chủ chặn qua thao tác 2 tab',
    300: 'Gửi duyệt = Lưu và gửi (Đang kiểm) + Cập nhật kết quả / Gửi duyệt (gửi Ban kiểm soát); Duyệt phiếu = Duyệt kết quả',
    301: 'lệch: Lưu và gửi / Gửi duyệt không có cửa sổ xác nhận — đúng theo code; Duyệt kết quả có popup ghi chú',
    307: 'duyệt có chênh > Chờ xử lý; không chênh > Hoàn thành; lập phiếu xử lý > Đang xử lý; xử lý hết > Hoàn thành',
    308: 'Gửi duyệt báo người có quyền Kế toán kho; Duyệt có chênh báo người xử lý (cùng công ty)',
    310: 'popup Hủy / rời màn chưa lưu', 313: 'nút Không duyệt ở màn chi tiết (trên dòng chỉ có Duyệt mở chi tiết)',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in list(range(142, 162)) + [179, 180, 271, 273, 277, 292]:
    TC_MAP[_stt] = NA_LOCK
for _stt in list(range(231, 268)) + [181, 275]:
    TC_MAP[_stt] = NA_IMPORT
_miss = [s for s in range(1, 325) if s not in TC_MAP]
assert not _miss, 'Thiếu dòng checklist Testcase: %s' % _miss

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.9.2; 2.10.2; 2.11.1; 2.12.2; 2.13.2; 2.14.2; 2.18.1'
NA_S_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dòng cuối ma trận Phần 2)'
NA_S_IMPORT = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'
UC = '2.5.1; 2.6.1; 2.7.1; 2.8.1; 2.9.1; 2.10.1; 2.12.1; 2.13.1; 2.14.1; 2.15.1; 2.16.1; 2.17.1'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2 (bảng Nhóm quyền quyết định phạm vi dữ liệu V1 / V2)', 12: 'Phần 2',
    13: 'Phần 2 (không có Khóa — ghi rõ dòng cuối ma trận)', 14: 'Phần 2 (không có Import; Xuất / Lịch sử theo phạm vi)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; ' + UC,
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.4.1; 2.5.2; 2.6.2; 2.7.2; 2.8.2; 2.9.2; 2.10.2; 2.12.2; 2.13.2; 2.14.2; 2.15.2; 2.16.2; 2.17.2; 2.18.1',
    23: SRS_INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.6.3 (2 lối vào); 2.8.3; 2.9.3',
    25: '2.1.2; 2.5.3; 2.6.3; 2.7.3; 2.10.3; 2.12.3; 2.13.3; 2.14.3; 2.15.3; 2.16.3; 2.18.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.1.4; 2.5.5; 2.12.5; 2.13.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; Phần 2', 53: '2.5.4; 2.7.4', 54: '2.5.4', 55: '2.5.2; Phần 4 — BR-09', 56: '2.5.4; 2.5.5; 2.7.5; 2.12.4',
    57: '2.5.5; 2.8.5', 58: '2.5.2; 2.5.5',
    59: '2.5.2 (màn Tạo là trang: không có (x) / click ngoài — ghi rõ cách rời màn); 2.6.2 (popup Chọn kế hoạch)',
    60: '2.5.2; 2.5.5', 61: '2.5.2; 2.5.5', 62: '2.5.5; 2.7.5',
    63: '2.9.2; Phần 2', 64: '2.9.2', 65: '2.9.2; 2.9.4', 66: '2.9.5', 67: '2.9.2; Phần 4 — BR-09', 68: '2.9.2', 69: '2.9.5',
    70: '2.9.2; 2.9.5', 71: '2.9.2 (không có Khóa; phiếu đã gửi không sửa được)', 72: '2.9.2; 2.18.1; Phần 4 — BR-14',
    73: '2.9.5',
    74: '2.10.2; 2.10.4', 75: '2.10.2; Phần 4 — BR-13', 76: '2.10.2; Phần 4 — BR-03',
    77: '2.10.2 (không có Khóa; phiếu đã gửi không xóa được)',
    78: '2.10.4', 79: '2.10.4', 80: '2.10.5', 81: '2.10.2; 2.10.5', 82: '2.10.5',
    83: 'Phần 1 (Thuật ngữ — các trạng thái); Phần 4 — BR-07',
    94: '2.18.1; 2.18.2', 95: '2.18.3', 96: '2.18.3', 97: '2.18.1; 2.18.3', 98: '2.18.3', 99: '2.18.1', 100: '2.18.1',
    101: '2.18.4',
    120: '2.17.2; 2.17.3', 121: '2.17.4', 122: '2.17.2; 2.17.4', 123: '2.17.4', 124: '2.17.4; 2.17.5', 125: '2.17.2',
    126: '2.17.2', 127: '2.17.2; 2.17.4', 128: '2.17.4', 129: '2.17.5',
    130: '2.11.1', 131: '2.11.2', 132: '2.11.3', 133: '2.11.1; 2.11.3',
    134: '2.11.1 (không có Khóa; nút theo trạng thái ghi ở 2.11.3)', 135: '2.11.3; 2.18.3', 136: '2.18.3',
    137: '2.11.1; 2.11.4', 138: '2.11.4',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-09', 148: 'Phần 4 — BR-09',
    149: 'N/A: không có Khóa và không có trường nhập duy nhất nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-13', 151: 'Phần 4 — BR-03; BR-05', 152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-10; BR-13; Phần 5', 154: 'Phần 4 — BR-14', 155: 'Phần 4 — BR-01 đến BR-14',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5; Phần 4 — BR-01 (số tồn là ảnh chụp)',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5; Phần 4 — BR-13', 163: 'Phần 5; Phần 4 — BR-13',
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
