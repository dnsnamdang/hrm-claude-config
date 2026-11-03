# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Hạch toán mua dịch vụ" với checklist "Mẫu tài liệu.xlsx" của tester (03/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
TC_MAP : dựng từ CK của gen_testcase.py (mỗi TC khai stt checklist nó phủ) + N/A + ghi chú lệch.
SRS_MAP: stt checklist SRS (1..163) -> mục trong SRS (2.x / 2.x.y / Phần n), hoặc 'N/A: <lý do>'.
Ghi chú trong ngoặc (lệch so với checklist, cách hiểu riêng của màn) ra cột Ghi chú.
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

NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (phiếu chỉ có 2 trạng thái Đang tạo, Đã duyệt)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_REJECT = ('N/A: màn không có chức năng Không duyệt — phiếu chỉ có Lưu nháp / Lưu và duyệt; trả phiếu về làm ở màn Yêu cầu hạch '
             'toán mua dịch vụ (trước khi lập phiếu hạch toán)')

# Ghi chú lệch / cách hiểu riêng, gắn sau danh sách TC.
NOTE = {
    16: 'lệch: số tổng ở dòng "Hiển thị a–b / N" chưa có dấu phẩy ngăn nghìn — lỗi chung đã ghi nhận',
    29: 'so khớp có dấu / không dấu theo cách so sánh chữ của cơ sở dữ liệu — chưa xác minh trên dev',
    31: 'lệch: ký tự % và _ được hiểu là ký tự đại diện — đúng theo code',
    33: 'lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code',
    45: 'bộ lọc chỉ nhớ 10 phút khi đi vào màn chi tiết / sửa / tạo của chính màn',
    46: 'F5 đưa bộ lọc về trống — đúng theo code',
    48: 'lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản',
    54: 'màn Tạo là trang: nút Lưu nháp / Lưu và duyệt / Lưu và tiếp tục / Quay lại',
    64: 'Diễn giải không có độ dài tối thiểu',
    67: 'phiếu không có trường nhập duy nhất, số phiếu tự sinh; mỗi phiếu yêu cầu chỉ 1 phiếu hạch toán',
    68: 'chưa xác minh bằng code việc bỏ khoảng trắng đầu / cuối của Diễn giải',
    76: 'màn Tạo là trang, không phải popup — kiểm vẫn ở màn Tạo',
    83: 'màn là trang: sau Lưu nháp chuyển về danh sách',
    86: 'màn không có "Lưu và gửi duyệt": nút tương ứng là Lưu và duyệt (ghi sổ)',
    87: 'nút tương ứng: Lưu và duyệt',
    88: 'nút tương ứng: Lưu và duyệt',
    89: 'nút tương ứng: Lưu và duyệt — trùng = 2 kế toán cùng lập từ 1 phiếu yêu cầu',
    90: 'màn là trang: sau Lưu và duyệt chuyển về danh sách',
    95: 'màn là trang, không có nút X — kiểm rời màn bằng menu, F5',
    103: 'màn Sửa là trang, không phải popup',
    116: 'không đổi được phiếu yêu cầu ở màn Sửa nên không thể trùng phiếu khác',
    126: 'màn không có trạng thái Khóa; trường hợp gần nhất: phiếu Đã duyệt không sửa được',
    127: 'câu lỗi "không tìm thấy bản ghi" là lỗi chung của máy chủ — chưa xác minh nguyên văn trên dev',
    138: 'câu lỗi "không tìm thấy bản ghi" là lỗi chung của máy chủ — chưa xác minh nguyên văn trên dev',
    186: 'màn chi tiết là trang, không phải popup',
    194: 'màn không có trạng thái Khóa; phiếu Đã duyệt (trạng thái cuối, chỉ xem)',
    196: 'màn chi tiết là trang: "đóng" là nút Quay lại',
    222: 'file rỗng chỉ có logo, tiêu đề, hàng tên cột (không có dòng "Không có dữ liệu")',
    278: 'phiếu không có trường Tên — kiểm sửa Diễn giải đồng bộ',
    279: 'số phiếu tự sinh, không sửa được — kiểm liên kết với phiếu yêu cầu',
    300: 'màn không có nút "Duyệt" riêng: Lưu và duyệt chính là duyệt',
    308: 'lệch: duyệt xong không gửi thông báo cho ai — đúng theo code',
    309: 'lệch: không có thông báo khi duyệt (xem dòng 308)',
}

TC_MAP = {}
for _stt, _ids in CK.items():
    _ref = ', '.join(dict.fromkeys(_ids))
    TC_MAP[_stt] = _ref + (' (%s)' % NOTE[_stt] if _stt in NOTE else '')
TC_MAP[137] = 'N/A: màn không có trạng thái Khóa; phiếu Đã duyệt không xóa được (TC_05.006)'
for _stt in (179, 180, 271, 273, 276, 277):
    TC_MAP[_stt] = NA_LOCK
for _stt in (181, 275):
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(142, 162):
    TC_MAP[_stt] = NA_LOCK
for _stt in range(231, 268):
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(313, 325):
    TC_MAP[_stt] = NA_REJECT

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.7.2; 2.10.2; 2.13.1'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Khóa / Mở khóa — ghi rõ dưới ma trận)',
    14: 'Phần 2 (không có Import; In, Xuất Excel, Lịch sử không gắn quyền riêng)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.6.1; 2.7.1; 2.8.1; 2.9.1; 2.10.1; 2.11.1; 2.12.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.4.1; 2.5.2; 2.10.2; 2.12.2',
    23: '2.1.1; 2.2.1; 2.5.2; 2.13.1 (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.10.3', 25: '2.1.2; 2.5.3; 2.8.3; 2.9.3; 2.11.3; 2.13.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.1.4; 2.5.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1; 2.2.3', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; 2.1.3', 53: '2.5.4', 54: '2.5.4', 55: '2.5.2; Phần 4 — BR-05, BR-10', 56: '2.5.4; 2.5.5', 57: '2.5.5',
    58: '2.5.4; 2.5.5', 59: '2.5.2 (màn Tạo là trang: không có (x) / click ngoài — ghi rõ cách rời màn)', 60: '2.5.2; 2.5.5',
    61: '2.5.2; 2.5.5', 62: '2.5.5',
    63: '2.7.2; 2.1.3', 64: '2.7.2; 2.7.5', 65: '2.7.2; 2.7.4', 66: '2.7.4; 2.7.5', 67: '2.7.2; Phần 4 — BR-10',
    68: '2.7.2 (phiếu yêu cầu khóa ở màn Sửa nên không trùng chính phiếu / phiếu khác)', 69: '2.7.2; 2.7.5', 70: '2.7.2; 2.7.5',
    71: '2.7.2 (không có Khóa; phiếu Đã duyệt coi như khóa sửa)', 72: '2.7.2; 2.13.1', 73: '2.7.5',
    74: '2.8.2; 2.8.4', 75: '2.8.2', 76: '2.8.2', 77: '2.8.2 (không có Khóa)', 78: '2.8.3; 2.8.4', 79: '2.8.4',
    80: '2.8.2; 2.8.4', 81: '2.8.2', 82: '2.8.5',
    83: 'Phần 1; Phần 4 — BR-04 (không có Khóa / Mở khóa; 2 trạng thái phiếu mô tả ở Thuật ngữ và BR-04)',
    94: '2.13.1; 2.13.2', 95: '2.13.3', 96: '2.13.3', 97: '2.13.1; 2.13.3', 98: '2.13.1; 2.13.3', 99: '2.13.1',
    100: '2.13.1', 101: '2.13.4',
    120: '2.12.2; 2.12.3', 121: '2.12.4', 122: '2.12.2; 2.12.4', 123: '2.12.4', 124: '2.12.4; 2.12.5', 125: '2.12.2',
    126: '2.12.2', 127: '2.12.2', 128: '2.12.2; 2.12.4', 129: '2.12.5',
    130: '2.9.2', 131: '2.9.3', 132: '2.9.4', 133: '2.9.2; 2.9.4',
    134: '2.9.2 (không có Khóa; phiếu Đã duyệt chỉ xem, chân màn chỉ In phiếu, Quay lại)',
    135: '2.9.4; 2.9.5', 136: '2.9.4; 2.13.3', 137: '2.9.2', 138: '2.9.5',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-10', 148: 'Phần 4 — BR-11',
    149: 'N/A: không có Khóa và không có trường nhập duy nhất nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-12', 151: 'Phần 4 — BR-04, BR-13; 2.8.2',
    152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-13; Phần 5', 154: 'Phần 4 — BR-14', 155: 'Phần 4 — BR-01 đến BR-09',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5', 163: 'Phần 5 (quan hệ chứng từ nguồn – chứng từ dùng lại ghi trong cột Màn hình)',
}
for _stt in range(84, 94):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
for _stt in range(102, 120):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'

if __name__ == '__main__':
    write(HERE, TC_MAP, SRS_MAP)
