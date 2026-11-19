# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Tổng hợp tiền về ngân hàng" với checklist "Mẫu tài liệu.xlsx" của tester (03/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
TC_MAP : stt checklist Testcase (1..324) -> TC ID trong testcase.xlsx, hoặc 'N/A: <lý do>'.
SRS_MAP: stt checklist SRS (1..163)      -> mục trong SRS (2.x / 2.x.y / Phần n), hoặc 'N/A: <lý do>'.
Ghi chú trong ngoặc (lệch so với checklist, cách hiểu riêng của màn) ra cột Ghi chú.
Màn CHỈ ĐỌC: không có Thêm mới, Chỉnh sửa, Xóa, Khóa/Mở khóa, Lịch sử thay đổi, Import Excel, Duyệt, Không duyệt.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from checklist_doi_chieu import write  # noqa: E402

NA_CREATE = ('N/A: màn không có chức năng Thêm mới (dòng tiền về sinh từ phiếu báo có đã duyệt; nút Tạo mới điều chỉnh công nợ '
             'chỉ chuyển dòng sang màn Phiếu yêu cầu điều chỉnh công nợ — kiểm ở nhóm VIII)')
NA_EDIT = 'N/A: màn không có chức năng Chỉnh sửa (màn chỉ đọc)'
NA_DEL = 'N/A: màn không có chức năng Xóa (TC_07.005 kiểm không có nút Xóa)'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (dòng chỉ có 2 trạng thái tính từ số tiền chưa điều chỉnh)'
NA_HIS = 'N/A: màn không có chức năng Lịch sử thay đổi (TC_07.005 kiểm không có nút Lịch sử)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_APPROVE = 'N/A: màn không có chức năng Duyệt phiếu (trạng thái dòng đổi khi phiếu kế toán điều chỉnh được duyệt — TC_06.004)'
NA_REJECT = 'N/A: màn không có chức năng Không duyệt phiếu'

TC_MAP = {
    # I. Hiển thị danh sách và truy cập
    1: 'TC_01.001, TC_01.002', 2: 'TC_01.003', 3: 'TC_01.004', 4: 'TC_01.005', 5: 'TC_01.006 (màn không có cột mặc định ẩn)',
    6: 'TC_01.007', 7: 'TC_01.008', 8: 'TC_01.009', 9: 'TC_01.010', 10: 'TC_01.001',
    11: 'TC_01.011', 12: 'TC_01.012', 13: 'TC_01.013', 14: 'TC_01.014', 15: 'TC_01.015', 16: 'TC_01.016',
    17: 'TC_01.017', 18: 'TC_01.011', 19: 'TC_01.018', 20: 'TC_01.019, TC_01.020', 21: 'TC_01.019, TC_01.020',
    22: 'TC_01.021 (màn chỉ có Ngày hạch toán, không có cột Ngày tạo / Ngày cập nhật)', 23: 'TC_01.022', 24: 'TC_01.023',
    25: 'TC_01.024',
    # II. Tìm kiếm và lọc
    26: 'TC_02.001', 27: 'TC_02.002', 28: 'TC_02.003', 29: 'TC_02.004 (số báo có không có dấu nên kiểm ở ô Ngân hàng)',
    30: 'TC_02.005',
    31: 'TC_02.006 (lệch: ký tự % và _ được hiểu là ký tự đại diện — gõ "_" ra toàn bộ dòng; đúng theo code)',
    32: 'TC_02.007', 33: 'TC_02.025 (lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code)',
    34: 'TC_02.008', 35: 'TC_02.009', 36: 'TC_02.010',
    37: 'TC_02.011, TC_02.012, TC_02.013, TC_02.014, TC_02.015, TC_02.016, TC_02.017',
    38: 'TC_02.019, TC_02.020', 39: 'TC_02.018', 40: 'TC_02.021', 41: 'TC_02.022', 42: 'TC_02.022', 43: 'TC_02.023',
    44: 'TC_02.024',
    45: 'TC_02.026 (lệch: màn KHÔNG giữ bộ lọc khi chuyển màn rồi quay lại — đúng theo code, expected có Lưu ý)',
    46: 'TC_02.027 (lệch: F5 làm mất bộ lọc — đúng theo code)',
    47: 'TC_02.028 (tab mới mở với bộ lọc trống — màn không ghi nhớ bộ lọc)',
    48: 'TC_02.029',
    # VII. Xem chi tiết (Xem phiếu báo có)
    186: 'TC_03.001 (màn chi tiết là trang của chức năng Phiếu báo có, không phải popup)', 187: 'TC_03.002',
    188: 'TC_03.003', 189: 'TC_03.004', 190: 'TC_03.005', 191: 'TC_03.006', 192: 'TC_03.007', 193: 'TC_03.004, TC_03.008',
    194: 'N/A: phiếu báo có / dòng tiền về không có trạng thái Khóa',
    195: 'TC_03.012 (khối Lịch sử là của phiếu báo có)',
    196: 'TC_03.009 (lệch: nút Quay lại của màn chi tiết về danh sách Phiếu báo có, không về màn Tổng hợp — đúng theo code)',
    197: 'TC_03.010 (lệch: quay lại bằng nút Lùi về trang 1, bộ lọc trống — đúng theo code)',
    # VIII. Tùy chỉnh cột
    198: 'TC_04.001', 199: 'TC_04.002', 200: 'TC_04.003', 201: 'TC_04.004', 202: 'TC_04.005', 203: 'TC_04.006',
    204: 'TC_04.007', 205: 'TC_04.008', 206: 'TC_04.009, TC_04.004, TC_04.005', 207: 'TC_04.010', 208: 'TC_04.011',
    209: 'TC_04.012', 210: 'TC_04.013', 211: 'TC_04.014',
    # IX. Xuất Excel
    212: 'TC_05.001', 213: 'TC_05.002',
    214: 'TC_05.003 (lệch: cửa sổ luôn tích cả 10 trường, không theo cột đang hiện trên bảng — đúng theo code)',
    215: 'TC_05.004', 216: 'TC_05.005', 217: 'TC_05.006', 218: 'TC_05.007', 219: 'TC_05.008', 220: 'TC_05.009',
    221: 'TC_05.010',
    222: 'TC_05.011 (file rỗng có logo, tiêu đề, hàng tên cột và dòng "Không có dữ liệu phù hợp")',
    223: 'TC_05.012', 224: 'TC_05.013', 225: 'TC_05.014', 226: 'TC_05.015', 227: 'TC_05.016', 228: 'TC_05.017',
    229: 'TC_05.018', 230: 'TC_05.019',
    # X. Ảnh hưởng các màn hình sử dụng dữ liệu
    268: 'N/A: màn không tạo bản ghi (dòng tiền về sinh khi phiếu báo có được duyệt — TC_06.001)',
    269: 'N/A: màn không tạo bản ghi cấp cha / con',
    270: 'TC_06.008', 271: NA_LOCK,
    272: 'TC_06.010 (màn không sửa dữ liệu; kiểm liên kết giữ nguyên khi dòng đổi trạng thái)', 273: NA_LOCK,
    274: 'TC_06.001, TC_06.002, TC_08.013', 275: NA_IMPORT, 276: NA_LOCK, 277: NA_LOCK,
    278: 'N/A: màn không sửa tên / nội dung dòng', 279: 'N/A: số báo có do màn Phiếu báo có sinh, không sửa trên màn này',
    280: 'TC_06.011', 281: 'TC_06.004, TC_06.005, TC_06.003, TC_06.006', 282: 'TC_06.007', 283: 'TC_06.009',
    284: 'TC_06.010', 285: 'TC_06.011', 286: 'TC_06.012, TC_06.013',
    # XI. Phân quyền
    287: 'TC_07.001, TC_07.002', 288: 'TC_07.004',
    289: 'TC_07.005 (màn không có Thêm mới — kiểm không có nút)', 290: 'TC_07.005 (màn không có Chỉnh sửa — kiểm không có nút)',
    291: 'TC_07.005 (màn không có Xóa — kiểm không có nút)', 292: 'TC_07.005 (màn không có Khóa / Mở khóa — kiểm không có nút)',
    293: 'TC_07.006, TC_07.007 (không có Import; Xuất Excel không gắn quyền riêng, xuất trong phạm vi công ty)',
    294: 'TC_07.005 (màn không có Lịch sử — kiểm không có nút)', 295: 'TC_07.008', 296: 'TC_07.009', 297: 'TC_07.007',
    298: 'TC_07.010, TC_07.011', 299: 'TC_07.002, TC_07.003, TC_07.011',
}
for _stt in range(49, 103):
    TC_MAP[_stt] = NA_CREATE
for _stt in range(103, 130):
    TC_MAP[_stt] = NA_EDIT
for _stt in range(130, 142):
    TC_MAP[_stt] = NA_DEL
for _stt in range(142, 162):
    TC_MAP[_stt] = NA_LOCK
for _stt in range(162, 186):
    TC_MAP[_stt] = NA_HIS
for _stt in range(231, 268):
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(300, 313):
    TC_MAP[_stt] = NA_APPROVE
for _stt in range(313, 325):
    TC_MAP[_stt] = NA_REJECT

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.6.2; 2.7.2'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Thêm, Sửa, Xóa, Khóa / Mở khóa — ghi rõ dưới ma trận)',
    14: 'Phần 2 (không có Import, Lịch sử; Xuất Excel không gắn quyền riêng)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.6.1; 2.7.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.4.1; 2.5.2; 2.7.2',
    23: '2.1.1; 2.2.1; 2.3.1; 2.4.1; 2.5.2; 2.6.2; 2.7.2 (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.6.3; 2.7.3', 25: '2.1.2; 2.3.2; 2.6.3; 2.7.3',
    26: '2.1.3; 2.2.3; 2.7.4', 27: '2.1.3; 2.2.3; 2.7.4', 28: '2.1.3; 2.2.3; 2.7.4', 29: '2.1.4; 2.7.5', 30: '2.1.4; 2.7.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1; 2.1.4', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1; 2.2.3', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    83: 'Phần 1 (Thuật ngữ — 2 trạng thái dòng); Phần 4 — BR-03 (không có Khóa / Mở khóa)',
    120: '2.5.2; 2.5.3', 121: '2.5.4', 122: '2.5.2; 2.5.4 (lệch: tích sẵn cả 10 trường, không theo cột đang hiện)',
    123: '2.5.4', 124: '2.5.4; 2.5.5', 125: '2.5.2', 126: '2.5.2', 127: '2.5.2', 128: '2.5.2; 2.5.4', 129: '2.5.5',
    130: '2.6.2', 131: '2.6.3', 132: '2.6.4', 133: '2.6.2; 2.6.4',
    134: 'N/A: phiếu báo có / dòng tiền về không có trạng thái Khóa',
    135: '2.6.4 (khối Lịch sử của phiếu báo có ở màn chi tiết; đặc tả đầy đủ theo SRS màn Phiếu báo có)',
    136: 'N/A: bộ lọc lịch sử thuộc màn Chi tiết phiếu báo có (SRS màn Phiếu báo có), màn này không có khối lịch sử riêng',
    137: '2.6.2 (lệch: không giữ trang / bộ lọc khi quay lại; Quay lại về danh sách Phiếu báo có — SRS ghi theo code)',
    138: '2.6.5',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-09', 148: 'Phần 4 — BR-07',
    149: 'N/A: không có Khóa và không nhập dữ liệu trên màn nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-10', 151: 'Phần 4 — BR-10 (màn không có Xóa; ghi ảnh hưởng khi phiếu báo có bị xóa / hủy)',
    152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-05; Phần 5', 154: 'Phần 4 — BR-12', 155: 'Phần 4 — BR-01 đến BR-13',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)', 162: 'Phần 5', 163: 'Phần 5 (quan hệ chứng từ nguồn – chứng từ dùng lại ghi trong cột Màn hình)',
}
for _stt in range(52, 63):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Thêm mới (Phần 1 Phạm vi chức năng; form tạo phiếu yêu cầu theo SRS màn đó — 2.7)'
for _stt in range(63, 74):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Chỉnh sửa (ghi rõ ở Phần 1 Phạm vi chức năng)'
for _stt in range(74, 83):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Xóa (ghi rõ ở Phần 1 và dưới ma trận Phần 2)'
for _stt in range(84, 94):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng)'
for _stt in range(94, 102):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Lịch sử thay đổi (Phần 1, Phần 4 — BR-12)'
for _stt in range(102, 120):
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'

if __name__ == '__main__':
    write(HERE, TC_MAP, SRS_MAP)
