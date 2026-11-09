# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Phiếu nhập hàng điều chỉnh kiểm kê" với checklist của tester (09/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../phieu-xuat-kho-dieu-chinh-kiem-ke/gen_checklist.py. SRS màn này có 12 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Cài đặt
bộ lọc · 2.4 Tùy chỉnh cột · 2.5 Tạo mới (UC) · 2.6 Chỉnh sửa (UC) · 2.7 Lưu và duyệt (UC) · 2.8 Xem chi tiết (UC) · 2.9 In phiếu
(UC) · 2.10 In danh sách (UC) · 2.11 Xuất Excel (UC) · 2.12 Lịch sử.
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


NA_DEL = 'N/A: màn không có chức năng Xóa (giữ như hệ thống cũ)'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (phiếu chỉ có 2 trạng thái Đang tạo / Đã hạch toán)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_REJECT = 'N/A: màn không có chức năng Không duyệt — bước duyệt là nút Lưu và duyệt của người lập, không có nút trả phiếu về'

NOTE = {
    29: 'số phiếu có chữ Đ — ghi nhận kết quả so khớp Đ / D thực tế',
    31: 'lệch: ký tự % và _ được hiểu là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    45: 'bộ lọc chỉ nhớ 10 phút khi đi vào màn chi tiết / sửa của chính màn',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản',
    54: 'màn Tạo là trang: Lưu / Lưu và tiếp tục / Lưu và duyệt / Quay lại',
    67: 'không có trường nhập duy nhất; trùng kho kế toán trong 1 dòng bị chặn',
    75: 'trùng = phiếu nhập kho đã lập (biến khỏi ô chọn)', 82: 'trùng = phiếu nhập kho đã lập (biến khỏi ô chọn)',
    76: 'màn là trang: ở lại màn Thêm với form trống', 83: 'màn là trang: Lưu xong về danh sách',
    86: 'nút tương ứng: Lưu và duyệt (từ Thêm hoặc Sửa)', 89: 'phiếu nhập kho đã lập không còn trong ô chọn',
    90: 'màn là trang; hộp xác nhận Lưu và duyệt', 92: 'sau Lưu và duyệt về danh sách',
    95: 'màn là trang: không có nút X; kiểm hộp Thông tin chưa lưu',
    102: 'lệch: không chặn lập trùng từ 1 phiếu nhập kho — giữ như hệ thống cũ (đã chốt 30/10)',
    116: 'màn Sửa không có trường cần kiểm trùng', 126: 'không có Khóa: tương ứng phiếu đã hạch toán không sửa được',
    127: 'không có Xóa: tương ứng phiếu bị đổi trạng thái trong lúc sửa',
    173: 'phiếu lập ở hệ thống cũ chưa có mốc lịch sử',
    186: 'màn chi tiết là trang, không phải popup', 194: 'màn không có trạng thái Khóa — kiểm phiếu Đang tạo',
    196: 'màn chi tiết là trang: "đóng" là nút Quay lại',
    222: 'lệch: danh sách rỗng không ra file, báo "Không có dữ liệu để xuất" — đúng theo code',
    268: 'tương ứng: phiếu nhập kho chưa Chờ duyệt thì không lập được',
    270: 'màn không có Xóa — kiểm danh mục Kho kế toán không xóa được kho đã dùng trên phiếu',
    271: 'không có Khóa phiếu — kiểm kho kế toán bị khóa ở danh mục', 276: 'kho kế toán đã khóa không chọn mới được',
    272: 'tên hàng lưu cố định lúc lập', 279: 'mã / tên hàng lưu trên dòng phiếu',
    286: 'lệch: sửa phiếu Đang tạo cộng số đã xử lý lần nữa — giữ như hệ thống cũ (đã chốt 30/10)',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm phạm vi áp lại sau khi bị gỡ quyền',
    300: 'bước duyệt = nút Lưu và duyệt', 301: 'hộp Xác nhận lưu và duyệt',
    308: 'màn không gửi thông báo — TC kiểm không phát sinh thông báo', 309: 'màn không gửi thông báo',
    312: 'Người duyệt / Ngày duyệt ghi trên phiếu nhập kho nguồn',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in list(range(130, 142)) + [280, 291]:
    TC_MAP.setdefault(_stt, NA_DEL)
for _stt in list(range(142, 162)) + [179, 180, 273, 277, 292]:
    TC_MAP.setdefault(_stt, NA_LOCK)
for _stt in list(range(231, 268)) + [181, 275]:
    TC_MAP.setdefault(_stt, NA_IMPORT)
for _stt in range(313, 325):
    TC_MAP.setdefault(_stt, NA_REJECT)

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.6.2; 2.7.2; 2.8.2; 2.12.1'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Xóa / Khóa — ghi rõ dòng cuối ma trận)', 14: 'Phần 2 (không có Import)', 15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.6.1; 2.7.1; 2.8.1; 2.9.1; 2.10.1; 2.11.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.5.2; 2.6.2; 2.7.2; 2.11.2',
    23: SRS_INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.6.3', 25: '2.5.3; 2.7.3; 2.9.3; 2.12.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.5.5; 2.6.5; 2.7.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1; 2.2.3', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; 2.5.4', 53: '2.5.4', 54: '2.5.4; Phần 4 — BR-08', 55: '2.5.2; Phần 4 — BR-02', 56: '2.5.4; 2.5.5; 2.7.5',
    57: '2.5.2; 2.5.5', 58: '2.5.2; 2.5.5 (Lưu và tiếp tục)', 59: '2.5.4; 2.5.5 (màn là trang: nút Quay lại + hộp Thông tin chưa lưu)',
    60: '2.5.2; 2.5.5; 2.6.5', 61: '2.5.5; 2.12.1', 62: '2.5.5; 2.6.5; 2.7.5',
    63: '2.6.2; 2.6.3', 64: '2.6.2; 2.6.4', 65: '2.6.4', 66: '2.6.4; 2.6.5',
    67: '2.6.4 (màn Sửa không có trường cần kiểm trùng)', 68: '2.6.4 (không áp dụng trùng)', 69: '2.6.2; 2.6.5',
    70: '2.6.2; 2.6.5', 71: '2.6.2 (không có Khóa: phiếu đã hạch toán không sửa được — Phần 4 BR-08)', 72: '2.6.2; 2.12.1',
    73: '2.6.5',
    83: 'Phần 1 Thuật ngữ; Phần 4 — BR-06 (không có Khóa / Mở khóa; 2 trạng thái phiếu)',
    94: '2.12.1; 2.12.2', 95: '2.12.3', 96: '2.12.3', 97: '2.12.1; 2.12.3', 98: '2.12.1; 2.12.3', 99: '2.12.1',
    100: '2.12.1', 101: '2.12.4',
    120: '2.11.2; 2.11.3', 121: '2.11.4', 122: '2.11.2; 2.11.4', 123: '2.11.4', 124: '2.11.4; 2.11.5', 125: '2.11.2; 2.10.2',
    126: '2.11.2; 2.10.2', 127: '2.11.2; 2.11.4', 128: '2.11.4', 129: '2.11.5',
    130: '2.8.2', 131: '2.8.3', 132: '2.8.4', 133: '2.8.2; 2.8.4', 134: '2.8.2 (không có Khóa; phiếu chỉ xem)',
    135: '2.8.4; 2.12.3', 136: '2.12.3', 137: '2.8.2; 2.8.5', 138: '2.8.5',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-09, BR-03', 148: 'Phần 4 — BR-08, BR-03',
    149: 'N/A: không có Khóa và không có trường nhập duy nhất nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-03, BR-07', 151: 'Phần 4 — BR-06 (màn không có Xóa)',
    152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-13; Phần 5', 154: 'Phần 4 — BR-12', 155: 'Phần 4 — BR-01 đến BR-13',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5 (sửa phiếu Đang tạo ghi lại dòng hàng + phân bổ)',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5 (màn không có Xóa; danh mục Kho kế toán / Kho vật lý / Vị trí chặn xóa khi đã dùng trên phiếu)',
    163: 'Phần 5; Phần 4 — BR-03, BR-07',
}
for _stt in range(74, 83):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Xóa (ghi rõ ở Phần 1 Phạm vi chức năng)'
for _stt in range(84, 94):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
for _stt in range(102, 120):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'

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
