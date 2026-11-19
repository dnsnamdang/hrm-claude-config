# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Phiếu giao việc" (lối vào ?type=all) với checklist của tester (19/11/2026).

Chạy: python gen_checklist.py -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
Hàm ghi dùng chung checklist_doi_chieu.write() đặt tên "Đối chiếu checklist.xlsx" trong thư mục truyền vào → ghi thẳng vào thư mục này
(file của bộ "Phiếu giao việc được giao" có tên riêng, không bị đè). Khuôn: gen_checklist_duoc_giao.py + ../finance-bill-adjust-dept/gen_checklist.py.
SRS màn này có 12 chức năng: 2.1 Xem DS · 2.2 Tìm kiếm · 2.3 Cài đặt bộ lọc · 2.4 Tùy chỉnh cột · 2.5 Tạo phiếu giao việc (UC) ·
2.6 Xem chi tiết · 2.7 Xóa (UC) · 2.8 Lịch sử · 2.9 Nhập kết quả (UC) · 2.10 Xem phiếu nhập kết quả · 2.11 In danh sách (UC) · 2.12 Xuất Excel (UC).
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
from gen_testcase import CK, OUT as TC_FILE  # noqa: E402

SRS_FILE = os.path.join(HERE, 'SRS - Phiếu giao việc.docx')

NA_EDIT = 'N/A: màn không có Chỉnh sửa (giữ như hệ thống ERP — không có lối vào Sửa)'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_CONT = 'N/A: màn Tạo không có "Lưu và tiếp tục" (lập từ 1 chứng từ nguồn, lưu là duyệt — user chốt 02/11/2026)'
NA_DRAFT = 'N/A: màn Tạo không có "Lưu nháp" (phiếu giao việc không có trạng thái nháp)'
NA_REJECT = 'N/A: màn không có Không duyệt phiếu (lưu là duyệt luôn)'

NOTE = {
    5: 'màn không có cột ẩn mặc định',
    29: 'số phiếu không có chữ có dấu',
    31: 'lệch: ký tự % và _ là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn ký tự — đúng theo code',
    45: 'lệch: chỉ giữ bộ lọc khi mở chi tiết rồi quay lại; sang màn khác thì mất — đúng theo code',
    46: 'lệch: F5 không giữ bộ lọc nếu chưa mở chi tiết — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản — đúng theo code',
    49: 'màn Tạo là trang, mở từ Phiếu chờ giao việc / phiếu yêu cầu; danh sách không có nút Tạo mới',
    54: 'màn Tạo là trang: nút Lưu và duyệt / Quay lại; không có Lưu nháp, Lưu và tiếp tục',
    64: 'ô chữ không có độ dài tối thiểu',
    67: 'phiếu không có trường nhập duy nhất, mã phiếu tự sinh — giao nhiều lần cùng chứng từ được',
    86: 'nút tương ứng: Lưu và duyệt (lưu là duyệt)', 87: 'nút tương ứng: Lưu và duyệt', 88: 'nút tương ứng: Lưu và duyệt',
    89: 'nút tương ứng: Lưu và duyệt — không có ràng buộc trùng',
    90: 'màn là trang: sau Lưu và duyệt chuyển về danh sách', 91: 'màn là trang: không làm mới form, về danh sách',
    92: 'màn là trang: sau lưu về danh sách',
    95: 'màn Tạo là trang, không có nút X — rời màn bằng Quay lại / menu',
    100: 'không có hết hạn phiên riêng của form; kiểm dữ liệu nguồn đổi trong lúc mở lâu',
    186: 'chi tiết là trang, không phải popup',
    196: 'chi tiết là trang: "đóng" là nút Quay lại',
    222: 'lệch: xuất rỗng không ra file, báo "Không có dữ liệu để xuất" — đúng theo code',
    268: 'tương ứng: điều kiện hiện Nhập kết quả; chứng từ chưa giao có ở Phiếu chờ giao việc',
    269: 'tương ứng: phiếu mới chọn được ở Phiếu giao công tác; mở màn Tạo phiếu nhập kết quả',
    270: 'tương ứng: đã gắn phiếu giao công tác thì không xóa được',
    272: 'mã phiếu tự sinh, không đổi; liên kết chứng từ nguồn giữ nguyên',
    278: 'phiếu không có trường Tên — kiểm thông tin khách hàng chép lúc lập không đổi theo chứng từ',
    279: 'mã phiếu tự sinh, không sửa được',
    297: 'skill chốt 03/11 không viết case gọi thẳng hệ thống — kiểm bị gỡ quyền giữa lúc thao tác',
    300: 'màn không có nút "Duyệt" riêng: Lưu và duyệt chính là duyệt',
    306: 'Lưu và duyệt ghi tiến độ giao việc, trừ SL còn của chứng từ nguồn',
    307: 'chứng từ nguồn đổi trạng thái / rời Phiếu chờ giao việc',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
for _stt in range(72, 79):
    TC_MAP.setdefault(_stt, NA_CONT)
for _stt in range(79, 86):
    TC_MAP.setdefault(_stt, NA_DRAFT)
for _stt in (90, 91, 92):
    TC_MAP.setdefault(_stt, 'TC_03.005 (%s)' % NOTE[_stt])
TC_MAP.setdefault(86, 'TC_03.005, TC_03.006 (%s)' % NOTE[86])
for _stt in range(103, 130):
    TC_MAP.setdefault(_stt, NA_EDIT)
for _stt in list(range(142, 162)) + [179, 180, 194, 271, 273, 276, 277, 292]:
    TC_MAP[_stt] = NA_LOCK
for _stt in [177, 178]:
    TC_MAP[_stt] = NA_EDIT + ' (mốc Tạo mới / Xóa kiểm ở TC_05.002, TC_05.006)'
for _stt in [181, 275] + list(range(231, 268)):
    TC_MAP.setdefault(_stt, NA_IMPORT)
TC_MAP.setdefault(308, 'N/A: lưu phiếu giao việc không gửi thông báo (giữ như ERP); thông báo chỉ có ở bước gửi duyệt phiếu nhập kết quả')
TC_MAP.setdefault(309, 'N/A: không có thông báo khi lưu phiếu giao việc')
for _stt in range(313, 325):
    TC_MAP.setdefault(_stt, NA_REJECT)
TC_MAP.setdefault(137, 'N/A: không có trạng thái Khóa; phiếu đã có kết quả không xóa được (TC_04.008)')
TC_MAP.setdefault(276, NA_LOCK)

INTRO = '2.1.1; 2.2.1; 2.3.1; 2.4.1; 2.5.2; 2.6.1; 2.7.2; 2.8.1; 2.9.2; 2.10.1; 2.11.2; 2.12.2'
UI = '2.1.3; 2.2.3; 2.3.3; 2.4.3; 2.5.4; 2.6.3; 2.7.4; 2.8.3; 2.9.4; 2.10.3; 2.11.4; 2.12.4'
EV = '2.1.4; 2.2.4; 2.3.4; 2.4.4; 2.5.5; 2.6.4; 2.7.5; 2.8.4; 2.9.5; 2.10.4; 2.11.5; 2.12.5'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Sửa / Khóa — ghi dòng cuối ma trận)', 14: 'Phần 2 (không có Import)', 15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3 sơ đồ tổng quan; 2.5.1; 2.7.1; 2.9.1; 2.11.1; 2.12.1',
    18: INTRO, 19: INTRO, 20: INTRO, 21: INTRO, 22: INTRO, 23: INTRO + ' (đoạn "Quy tắc chung" có liên kết)',
    24: '2.1.2 (lối vào + phạm vi); 2.5.3 (lối vào màn Tạo); 2.6.2', 25: '2.1.2 (trạng thái rỗng); 2.5.3 (lỗi kiểm tra, hộp xác nhận, chưa lưu); 2.7.3; 2.11.3',
    26: UI, 27: UI, 28: UI, 29: EV, 30: EV,
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1 (Yêu cầu đặc biệt); 2.1.3; 2.4.3', 34: '2.1.3', 35: '2.1.1; 2.1.3; 2.1.4',
    36: '2.1.3', 37: '2.1.3', 38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1 (Yêu cầu đặc biệt)', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3',
    45: '2.2.3', 46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2 (điều kiện tạo theo loại nguồn; màn Tạo là trang, không phải popup); Phần 4 — BR-02', 53: '2.5.4', 54: '2.5.2; 2.5.4',
    55: '2.5.2 (Yêu cầu đặc biệt); Phần 4 — BR-14 (không có trường duy nhất)', 56: '2.5.4; 2.5.5; Phần 4 — BR-04',
    57: '2.5.2; 2.5.5 (nút Lưu và duyệt)', 58: 'N/A: màn Tạo không có Lưu và tiếp tục (2.5.2 Yêu cầu đặc biệt)',
    59: '2.5.2 (màn Tạo là trang: rời bằng Quay lại / menu)', 60: '2.5.2; 2.5.4; 2.5.5 (hộp Thông tin chưa lưu)',
    61: '2.5.5; Phần 4 — BR-05, BR-12', 62: '2.5.5',
    74: '2.7.2; Phần 4 — BR-08', 75: '2.7.2 (trả số lượng chứng từ nguồn); Phần 4 — BR-08', 76: '2.7.2; Phần 4 — BR-08 (đã gắn phiếu giao công tác thì không xóa)',
    77: 'N/A: màn không có trạng thái Khóa', 78: '2.7.4', 79: '2.7.4', 80: '2.7.2; 2.7.4', 81: '2.7.2; 2.7.5', 82: '2.7.5',
    83: 'Phần 1 Thuật ngữ (8 trạng thái + Hủy); Phần 4 — BR-09 (không có Khóa / Mở khóa)',
    94: '2.8.1; 2.8.2', 95: '2.8.3', 96: '2.8.3', 97: '2.8.3', 98: '2.8.3', 99: '2.8.1', 100: '2.8.1; 2.8.4', 101: '2.8.4',
    120: '2.12.2; 2.12.3', 121: '2.12.4', 122: '2.12.2; 2.12.4', 123: '2.12.4', 124: '2.12.4; 2.12.5', 125: '2.12.2',
    126: '2.12.2 (rỗng không ra file — đúng theo code)', 127: '2.12.2; 2.12.4', 128: '2.12.4', 129: '2.12.5',
    130: '2.6.1', 131: '2.6.2', 132: '2.6.3', 133: '2.6.3', 134: 'N/A: phiếu giao việc không có trạng thái Khóa',
    135: '2.6.3; 2.8.3', 136: '2.8.3', 137: '2.6.1; 2.6.4', 138: '2.6.4',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-14', 148: 'Phần 4 — BR-14', 149: 'N/A: không có Khóa nên không có trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-03, BR-09; Phần 1 Thuật ngữ (Cấu trúc phân cấp)', 151: 'Phần 4 — BR-08', 152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-05, BR-09; Phần 5', 154: 'Phần 4 — BR-12', 155: 'Phần 4 — BR-01 đến BR-14',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5 (màn không sửa phiếu; thông tin chép lúc lập, chứng từ nguồn quyết định khách, SL)',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5; Phần 4 — BR-08 (đã gắn phiếu giao công tác thì không xóa)', 163: 'Phần 5; Phần 4 — BR-03, BR-09',
}
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
    out = write(HERE, TC_MAP, SRS_MAP, testcase=TC_FILE, srs=SRS_FILE)
    tc_na = sum(1 for v in TC_MAP.values() if v.startswith('N/A'))
    srs_na = sum(1 for v in SRS_MAP.values() if v.startswith('N/A'))
    print('Testcase: %d có TC / %d N/A; SRS: %d có mục / %d N/A -> %s'
          % (len(TC_MAP) - tc_na, tc_na, len(SRS_MAP) - srs_na, srs_na, out))
