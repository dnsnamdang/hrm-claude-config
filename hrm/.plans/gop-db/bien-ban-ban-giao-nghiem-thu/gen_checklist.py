# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Biên bản bàn giao nghiệm thu" với checklist của tester (10/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Checklist chuẩn (chốt 03/11/2026): .claude/skills/testcase-documenter/assets/CHECKLIST_TC_SRS.xlsx (tab Testcase + tab SRS);
hàm ghi dùng chung checklist_doi_chieu.write() đọc bản JSON (324 case + 163 mục SRS) — _assert_checklist_moi() dừng nếu 2 bản lệch.
TC_MAP : dựng từ CK của gen_testcase.py + N/A + ghi chú lệch. SRS_MAP: stt checklist SRS -> mục trong SRS.
Khuôn: ../phieu-nhap-hang-dieu-chinh-kiem-ke/gen_checklist.py. SRS màn này có 14 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Cài đặt
bộ lọc · 2.4 Tùy chỉnh cột · 2.5 Tạo mới (UC) · 2.6 Chọn hợp đồng (UC) · 2.7 Chỉnh sửa (UC) · 2.8 Lưu và duyệt (UC) · 2.9 Xóa (UC) ·
2.10 Xem chi tiết (UC) · 2.11 In biên bản (UC) · 2.12 In danh sách (UC) · 2.13 Xuất Excel (UC) · 2.14 Lịch sử.
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


NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (biên bản chỉ có trạng thái Đang tạo / Chờ duyệt / Đã duyệt)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_REJECT = ('N/A: màn không có chức năng Không duyệt — bước duyệt là nút Lưu và duyệt của người lập (giữ như hệ thống cũ), không có '
             'nút trả biên bản về')

NOTE = {
    29: 'số hợp đồng có chữ Đ — ghi nhận kết quả so khớp Đ / D thực tế',
    31: 'lệch: ký tự % và _ được hiểu là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    45: 'bộ lọc chỉ nhớ 10 phút khi đi vào màn chi tiết / sửa của chính màn, riêng từng lối vào',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản',
    54: 'màn Tạo là trang: Lưu nháp / Lưu và duyệt / Lưu và tiếp tục / Quay lại',
    67: 'trường duy nhất = Hợp đồng (1 hợp đồng – 1 biên bản)',
    76: 'màn là trang: ở lại màn Tạo với form trống', 83: 'màn là trang: Lưu nháp xong về danh sách',
    86: 'nút tương ứng: Lưu và duyệt (từ Tạo hoặc Sửa)', 89: 'hợp đồng đã lập không còn trong popup',
    90: 'màn là trang; hộp Xác nhận lưu và duyệt', 92: 'sau Lưu và duyệt về danh sách',
    95: 'màn là trang: không có nút X; kiểm hộp Thông tin chưa lưu',
    113: 'ô Hợp đồng không bỏ trống được ở màn Sửa (chỉ chọn lại)',
    126: 'không có Khóa: tương ứng biên bản Đã duyệt / của người khác không sửa được',
    135: 'không có ràng buộc "đang sử dụng" chặn xóa; biên bản Đã duyệt không có nút Xóa',
    136: 'không có dữ liệu con chặn xóa — xóa kèm dòng hàng, dòng chi tiết',
    137: 'không có Khóa — kiểm biên bản Đã duyệt không xóa được',
    173: 'biên bản lập ở hệ thống cũ chưa có mốc lịch sử',
    186: 'màn chi tiết là trang, không phải popup', 194: 'màn không có trạng thái Khóa — kiểm biên bản Đang tạo',
    196: 'màn chi tiết là trang: "đóng" là nút Quay lại',
    222: 'lệch: Xuất Excel rỗng không ra file, báo "Không có dữ liệu để xuất"; In danh sách rỗng chỉ có tiêu đề — đúng theo code',
    268: 'tương ứng: hợp đồng còn hàng chưa xuất / chưa hiệu lực thì không lập được',
    270: 'màn không có trường khóa — kiểm danh mục hàng hóa không xóa được hàng đã có trên biên bản',
    272: 'số hợp đồng lưu cố định lúc lập', 279: 'số hợp đồng, tên hàng lưu trên biên bản',
    280: 'xóa biên bản giải phóng hợp đồng để lập lại', 286: '1 hợp đồng – 1 biên bản',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm từ chối khi bị gỡ quyền',
    300: 'bước duyệt = nút Lưu và duyệt', 301: 'hộp Xác nhận lưu và duyệt',
    302: 'giữ như hệ thống cũ: không cần quyền duyệt riêng (đã chốt 03/11/2026)',
    308: 'màn không gửi thông báo — TC kiểm không phát sinh thông báo', 309: 'màn không gửi thông báo',
    312: 'người duyệt / thời điểm = mốc Thay đổi trạng thái trong lịch sử',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in list(range(142, 162)) + [179, 180, 271, 273, 277, 292]:
    TC_MAP.setdefault(_stt, NA_LOCK)
for _stt in list(range(231, 268)) + [181, 275]:
    TC_MAP.setdefault(_stt, NA_IMPORT)
for _stt in range(313, 325):
    TC_MAP.setdefault(_stt, NA_REJECT)

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.6.2; 2.7.2; 2.8.2; 2.9.2; 2.10.2; 2.14.1'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Khóa / Import / Không duyệt — ghi rõ dòng cuối ma trận)', 14: 'Phần 2 (không có Import)', 15: 'Phần 2',
    16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.6.1; 2.7.1; 2.8.1; 2.9.1; 2.10.1; 2.11.1; 2.12.1; 2.13.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.5.2; 2.7.2; 2.8.2; 2.13.2',
    23: SRS_INTRO + ' (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2 (3 lối vào); 2.5.3; 2.7.3', 25: '2.1.2; 2.5.3; 2.6.3; 2.8.3; 2.9.3; 2.11.3; 2.14.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.5.5; 2.7.5; 2.8.5; 2.9.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.2', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1; 2.2.3', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; 2.5.4', 53: '2.5.4', 54: '2.5.4; Phần 4 — BR-04, BR-05', 55: '2.5.2; Phần 4 — BR-03', 56: '2.5.4; 2.5.5; 2.6.5',
    57: '2.5.2; 2.5.5', 58: '2.5.2; 2.5.5 (Lưu và tiếp tục)', 59: '2.5.4; 2.5.5 (màn là trang: nút Quay lại + hộp Thông tin chưa lưu)',
    60: '2.5.2; 2.5.5; 2.7.5', 61: '2.5.5; 2.14.1', 62: '2.5.5; 2.6.5; 2.7.5; 2.8.5',
    63: '2.7.2; 2.7.3', 64: '2.7.2; 2.7.4', 65: '2.7.4', 66: '2.7.4; 2.7.5',
    67: '2.7.4; 2.7.5 (hợp đồng đã có biên bản khác)', 68: '2.7.5 (popup loại trừ chính biên bản đang sửa)', 69: '2.7.2; 2.7.5',
    70: '2.7.2; 2.7.5', 71: '2.7.2 (không có Khóa: biên bản Đã duyệt không sửa được — Phần 4 BR-07)', 72: '2.7.2; 2.14.1',
    73: '2.7.5',
    74: '2.9.2; 2.9.4', 75: '2.9.2 (xóa kèm dòng hàng, dòng chi tiết — không có dữ liệu con chặn xóa); Phần 4 — BR-07',
    76: '2.9.2 (Dòng sự kiện phụ / Yêu cầu đặc biệt); Phần 4 — BR-07',
    77: '2.9.2 (không có Khóa: biên bản Đã duyệt / Chờ duyệt không xóa được)', 78: '2.9.4', 79: '2.9.4', 80: '2.9.2; 2.9.5',
    81: '2.9.2; 2.9.5', 82: '2.9.5',
    83: 'Phần 1 Thuật ngữ; Phần 4 — BR-08 (không có Khóa / Mở khóa; 3 trạng thái biên bản)',
    94: '2.14.1; 2.14.2', 95: '2.14.3', 96: '2.14.3', 97: '2.14.1; 2.14.3', 98: '2.14.1; 2.14.3', 99: '2.14.1',
    100: '2.14.1', 101: '2.14.4',
    120: '2.13.2; 2.13.3', 121: '2.13.4', 122: '2.13.2; 2.13.4', 123: '2.13.4', 124: '2.13.4; 2.13.5', 125: '2.13.2; 2.12.2',
    126: '2.13.2; 2.12.2', 127: '2.13.2; 2.13.4', 128: '2.13.4', 129: '2.13.5',
    130: '2.10.2', 131: '2.10.3', 132: '2.10.4', 133: '2.10.2; 2.10.4', 134: '2.10.2 (không có Khóa; biên bản chỉ xem)',
    135: '2.10.4; 2.14.3', 136: '2.14.3', 137: '2.10.2; 2.10.5', 138: '2.10.5',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-03', 148: 'Phần 4 — BR-09, BR-04',
    149: 'N/A: không có Khóa nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-06; Phần 1 Thuật ngữ (Cấu trúc phân cấp)', 151: 'Phần 4 — BR-07',
    152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-14; Phần 5', 154: 'Phần 4 — BR-13', 155: 'Phần 4 — BR-01 đến BR-14',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5 (số hợp đồng, thông tin khách lưu cố định trên biên bản)',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5 (Kho dữ liệu hàng hoá chặn xóa hàng đã có trên biên bản); Phần 4 — BR-14',
    163: 'Phần 5; Phần 4 — BR-06',
}
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
