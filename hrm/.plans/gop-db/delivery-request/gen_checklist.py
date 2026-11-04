# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn Phiếu yêu cầu vận chuyển, bốc xếp với checklist "Mẫu tài liệu.xlsx" (02/11/2026).

Chạy: python gen_checklist.py -> Đối chiếu checklist.xlsx
TC_MAP dựng từ COVER của gen_testcase.py (mỗi TC tự khai stt checklist nó kiểm) + N/A + ghi chú lệch bên dưới.
SRS_MAP khai tay theo mục của gen_srs.py (2.x.1..: chức năng có Use Case là 5, 6, 7, 8, 9, 10, 11, 12, 13 nên mục con
lệch 1 so với 1, 2, 3, 4, 14).
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
from gen_testcase import COVER  # noqa: E402

LOCK = 'N/A: màn không có chức năng Khóa/Mở khóa (phiếu chỉ có 4 trạng thái Đang tạo, Chờ duyệt, Đã duyệt, Từ chối)'
IMPORT = 'N/A: màn không có chức năng Nhập Excel (Import) — chỉ có Xuất Excel'

TC_NA = {s: LOCK for s in range(142, 162)}
TC_NA.update({s: IMPORT for s in range(231, 268)})
TC_NA.update({
    126: LOCK + '; phiếu Chờ duyệt / Đã duyệt không sửa được đã kiểm ở TC_04.027',
    137: LOCK + '; phiếu Chờ duyệt / Đã duyệt không xóa được đã kiểm ở TC_05.005',
    179: LOCK, 180: LOCK, 194: LOCK, 271: LOCK, 273: LOCK, 276: LOCK, 277: LOCK, 292: LOCK,
    181: IMPORT, 275: IMPORT,
    282: 'N/A: không màn nào khác có bộ lọc theo dữ liệu phiếu vận chuyển (màn Phiếu yêu cầu xuất hàng không có ô lọc '
         'theo hình thức vận chuyển)',
})

TC_NOTE = {
    29: 'chữ Đ và D là hai chữ khác nhau, gõ "HD" không ra "HĐ…" — đúng theo code',
    46: 'F5 khi chưa mở phiếu thì bộ lọc về trống; bộ lọc chỉ ghi nhớ khi mở Chi tiết / Sửa rồi quay lại',
    48: 'lệch: bộ lọc ghi nhớ theo trình duyệt, tài khoản khác đăng nhập cùng trình duyệt trong 10 phút thấy lại bộ lọc — đúng theo code',
    64: 'không có độ dài tối thiểu, 1 ký tự lưu được',
    67: 'phiếu không có trường duy nhất: 2 phiếu cùng nội dung đều lưu, mã khác nhau',
    75: 'phiếu không có trường duy nhất: lưu được, mã khác nhau',
    76: 'form Tạo là trang: Lưu và tiếp tục ở lại màn Tạo',
    82: 'phiếu không có trường duy nhất: lưu được, mã khác nhau',
    83: 'form Tạo là trang: Lưu nháp xong tự về danh sách',
    84: 'sau Lưu nháp về danh sách; Tạo mới lại thì form trống',
    89: 'phiếu không có trường duy nhất: gửi duyệt được, mã khác nhau',
    90: 'form Tạo là trang: Gửi duyệt xong tự về danh sách',
    91: 'sau Gửi duyệt về danh sách; Tạo mới lại thì form trống',
    95: 'màn Tạo là trang, không có nút X — kiểm bằng tải lại / đóng tab',
    103: 'màn Sửa là trang riêng, không phải popup',
    116: 'không kiểm trùng: chọn phiếu YCXH đã dùng ở phiếu khác vẫn lưu được',
    127: 'lệch: báo câu tiếng Anh "Item Not Found!" — đúng theo code, nghi lỗi hiển thị',
    129: 'phiếu Chờ duyệt / Đã duyệt không sửa được',
    135: 'không màn nào tham chiếu phiếu; phiếu Đã duyệt / Chờ duyệt không có nút Xóa',
    138: 'lệch: báo câu tiếng Anh "Item Not Found!" — đúng theo code, nghi lỗi hiển thị',
    163: 'lịch sử dạng dòng thời gian (thời điểm, hành động, người thực hiện, nội dung), không phải bảng cột',
    186: 'màn Chi tiết là trang riêng, không phải popup',
    196: 'màn Chi tiết là trang: đóng bằng Quay lại',
    197: 'lệch: giữ bộ lọc nhưng danh sách về trang 1 (không nhớ số trang) — đúng theo code',
    222: 'lệch: danh sách rỗng chỉ báo "Không có dữ liệu phù hợp.", KHÔNG tải file — đúng theo code',
    272: 'phiếu chỉ có trạng thái, không có Khóa',
    274: 'phiếu vận chuyển không hiện ở màn nào khác; tác động duy nhất là ô Vận chuyển của phiếu YCXH khi duyệt',
    293: 'màn chỉ có Xuất Excel, không có Import',
    303: 'duyệt không có trường phải nhập; bắt buộc đã kiểm lúc gửi duyệt',
    313: 'nghiệp vụ gọi là "Từ chối"',
}

TC_MAP = {}
for stt in range(1, 325):
    if stt in TC_NA:
        assert stt not in COVER, 'stt %d vừa có TC vừa N/A' % stt
        TC_MAP[stt] = TC_NA[stt]
        continue
    assert stt in COVER, 'stt %d chưa có TC' % stt
    ids = list(dict.fromkeys(COVER[stt]))[:4]
    TC_MAP[stt] = ', '.join(ids) + (' (%s)' % TC_NOTE[stt] if stt in TC_NOTE else '')

SRS_LOCK = 'N/A: màn không có chức năng Khóa/Mở khóa (Phần 1 phạm vi chức năng, Phần 2 ma trận ghi rõ)'
SRS_IMPORT = 'N/A: màn không có chức năng Nhập Excel (Phần 1 phạm vi chức năng, Phần 2 ma trận ghi rõ)'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1',
    5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2',
    12: 'Phần 2', 13: 'Phần 2 (Khóa/Mở khóa: màn không có, ghi trong ma trận)',
    14: 'Phần 2 (Nhập Excel: màn không có; Xuất Excel, Xem lịch sử có trong ma trận)', 15: 'Phần 2', 16: 'Phần 2',
    17: '2.5.1, 2.8.1, 2.9.1, 2.10.1, 2.11.1, 2.12.1, 2.13.1',
    18: '2.1.1, 2.5.2', 19: '2.1.1, 2.5.2', 20: '2.1.1, 2.5.2', 21: '2.1.1, 2.5.2', 22: '2.5.2, 2.8.2', 23: '2.1.1, 2.5.2',
    24: '2.1.2, 2.5.3', 25: '2.5.3, 2.10.3, 2.12.3',
    26: '2.1.3, 2.5.4', 27: '2.5.4', 28: '2.1.3, 2.5.4',
    29: '2.1.4, 2.5.5', 30: '2.5.5',
    31: '2.1.1, 2.1.2', 32: '2.1.3', 33: '2.1.1, 2.4.1', 34: '2.1.3',
    35: '2.1.1, 2.1.4', 36: '2.1.1, 2.1.3', 37: '2.1.3',
    38: '2.1.1', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1, 2.2.3', 42: '2.2.1', 43: '2.2.1',
    44: '2.2.3', 45: '2.2.1, 2.2.3', 46: '2.2.1', 47: '2.2.1, 2.2.4',
    48: '2.2.3', 49: '2.2.1', 50: '2.2.1, 2.1.3', 51: '2.2.4',
    52: '2.5.2', 53: '2.5.4', 54: '2.5.4',
    55: '2.5.2, Phần 4', 56: '2.5.4, 2.5.5',
    57: '2.5.2, 2.5.5', 58: '2.5.2, 2.5.5', 59: '2.5.2 (màn Tạo là trang riêng: không có X / click ngoài, ghi rõ trong Yêu cầu đặc biệt)',
    60: '2.5.2, 2.5.5',
    61: '2.5.2, 2.5.5', 62: '2.5.5',
    63: '2.8.2, 2.1.3', 64: '2.8.2, 2.8.5', 65: '2.8.2',
    66: '2.8.4, 2.8.5', 67: '2.8.2', 68: '2.8.2',
    69: '2.8.2, 2.8.5', 70: '2.8.5', 71: '2.8.2 (không có Khóa; phiếu Chờ duyệt / Đã duyệt không sửa được)',
    72: '2.8.2, 2.8.5', 73: '2.8.5',
    74: '2.9.2, 2.1.3', 75: '2.9.2', 76: '2.9.2',
    77: '2.9.2 (không có Khóa; phiếu Chờ duyệt / Đã duyệt không xóa được)',
    78: '2.9.2, 2.9.4', 79: '2.9.4', 80: '2.9.2, 2.9.5', 81: '2.9.2', 82: '2.9.5',
    83: 'Phần 1, Phần 4 (không có FR Khóa/Mở khóa; các trạng thái phiếu ghi ở Thuật ngữ và BR-06)',
    94: '2.14.1, 2.14.2', 95: '2.14.3', 96: '2.14.3', 97: '2.14.1, 2.14.3',
    98: '2.14.3', 99: '2.14.1', 100: '2.14.1', 101: '2.14.4',
    120: '2.13.2, 2.13.3', 121: '2.13.4', 122: '2.13.2, 2.13.4', 123: '2.13.2, 2.13.4', 124: '2.13.2, 2.13.4',
    125: '2.13.2', 126: '2.13.2 (lệch: danh sách rỗng KHÔNG tải file, chỉ báo "Không có dữ liệu phù hợp." — SRS ghi theo code)',
    127: '2.13.2', 128: '2.13.4', 129: '2.13.5',
    130: '2.10.2', 131: '2.10.3', 132: '2.10.4', 133: '2.10.2, 2.10.4',
    134: 'N/A: màn không có trạng thái Khóa; phiếu Đã duyệt xem bình thường ở 2.10',
    135: '2.10.4', 136: '2.10.4, 2.14.3',
    137: '2.10.2 (lệch: quay lại giữ bộ lọc nhưng về trang 1 — SRS ghi theo code)', 138: '2.10.5',
    139: '2.4.1, 2.4.3', 140: '2.4.1, 2.4.3', 141: '2.4.1, 2.4.3', 142: '2.4.3, 2.4.4',
    143: '2.4.1, 2.4.4', 144: '2.4.1', 145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4', 148: 'Phần 4', 149: 'Phần 4 (BR-14: không có Khóa nên không có quy tắc trùng bản ghi đã khóa)',
    150: 'Phần 4', 151: 'Phần 4', 152: 'N/A: màn không có chức năng Khóa/Mở khóa',
    153: 'Phần 4, Phần 5', 154: 'Phần 4', 155: 'Phần 4',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)', 162: 'Phần 5', 163: 'Phần 5, Phần 4',
}
SRS_MAP.update({s: SRS_LOCK for s in range(84, 94)})
SRS_MAP.update({s: SRS_IMPORT for s in range(102, 120)})

if __name__ == '__main__':
    write(HERE, TC_MAP, SRS_MAP)
