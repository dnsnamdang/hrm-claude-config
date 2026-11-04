# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Phiếu yêu cầu hạch toán bổ sung" với checklist "Mẫu tài liệu.xlsx" của tester (02/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
TC_MAP : stt checklist Testcase (1..324) -> TC ID trong testcase.xlsx, hoặc 'N/A: <lý do>'.
SRS_MAP: stt checklist SRS (1..163)      -> mục trong SRS (2.x / 2.x.y / Phần n), hoặc 'N/A: <lý do>'.
Ghi chú trong ngoặc (lệch so với checklist, cách hiểu riêng của màn) ra cột Ghi chú.
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

NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (phiếu chỉ có 4 trạng thái Đang tạo, Chờ duyệt, Đang duyệt, Đã duyệt)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'

TC_MAP = {
    # I. Hiển thị danh sách và truy cập
    1: 'TC_01.001, TC_01.002', 2: 'TC_01.003', 3: 'TC_01.004', 4: 'TC_01.005', 5: 'TC_01.006',
    6: 'TC_01.007, TC_01.008', 7: 'TC_01.009', 8: 'TC_01.010', 9: 'TC_01.011', 10: 'TC_01.001',
    11: 'TC_01.012', 12: 'TC_01.013', 13: 'TC_01.014', 14: 'TC_01.015', 15: 'TC_01.016',
    16: 'TC_01.001, TC_02.019 (lệch: số tổng ở dòng "Hiển thị a–b / N" chưa có dấu phẩy ngăn nghìn — lỗi chung đã ghi nhận)',
    17: 'TC_01.017', 18: 'TC_01.012', 19: 'TC_01.001', 20: 'TC_01.018', 21: 'TC_01.018', 22: 'TC_01.019',
    23: 'TC_01.020', 24: 'TC_01.021', 25: 'TC_01.022',
    # II. Tìm kiếm và lọc
    26: 'TC_02.001', 27: 'TC_02.002', 28: 'TC_02.003',
    29: 'TC_02.004 (số phiếu không có dấu nên kiểm ở ô Diễn giải; chữ "đ" khác "d" khi tìm)',
    30: 'TC_02.005',
    31: 'TC_02.006 (lệch: ký tự % và _ được hiểu là ký tự đại diện — gõ "%" ra toàn bộ phiếu; đúng theo code hiện tại)',
    32: 'TC_02.007',
    33: 'TC_02.034 (lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code)',
    34: 'TC_02.008', 35: 'TC_02.009', 36: 'TC_02.010',
    37: 'TC_02.011, TC_02.012, TC_02.013, TC_02.014, TC_02.015, TC_02.016, TC_02.017, TC_02.024',
    38: 'TC_02.032, TC_02.033', 39: 'TC_02.031', 40: 'TC_02.018', 41: 'TC_02.019', 42: 'TC_02.019', 43: 'TC_02.020',
    44: 'TC_02.021, TC_01.025',
    45: 'TC_02.026, TC_02.027, TC_02.028 (bộ lọc chỉ được nhớ 10 phút khi đi vào màn chi tiết / sửa; sang màn khác thì xóa)',
    46: 'TC_02.035 (F5 đưa bộ lọc về trống — đúng theo code)',
    47: 'TC_02.030',
    48: 'TC_02.029 (lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản — trong 10 phút tài khoản khác có thể thấy bộ lọc '
        'cũ; expected ghi theo yêu cầu, có dòng Lưu ý)',
    # III. Thêm mới
    49: 'TC_03.001', 50: 'TC_03.002', 51: 'TC_03.003, TC_03.007', 52: 'TC_03.004', 53: 'TC_03.005', 54: 'TC_03.006',
    55: 'TC_03.008', 56: 'TC_03.009', 57: 'TC_03.010', 58: 'TC_03.011', 59: 'TC_03.012', 60: 'TC_03.013',
    61: 'TC_03.014', 62: 'TC_03.015, TC_03.016', 63: 'TC_03.017',
    64: 'TC_03.018 (không có độ dài tối thiểu)',
    65: 'TC_03.019, TC_03.063 (Diễn giải không có độ dài tối đa; giới hạn có thật của form là file tối đa 20MB)',
    66: 'TC_03.020, TC_03.063 (lệch: ô Diễn giải không giới hạn số ký tự — đúng theo code)',
    67: 'TC_03.021, TC_03.022 (phiếu không có trường duy nhất, mã tự sinh; chỉ chặn trùng cặp đối tượng – hợp đồng trong cùng phiếu)',
    68: 'TC_03.023', 69: 'TC_03.024', 70: 'TC_03.025', 71: 'TC_03.026',
    72: 'TC_03.027', 73: 'TC_03.028, TC_03.029', 74: 'TC_03.030', 75: 'TC_03.031',
    76: 'TC_03.032 (màn Tạo là trang, không phải popup — kiểm vẫn ở màn Tạo)', 77: 'TC_03.033', 78: 'TC_03.034',
    79: 'TC_03.035', 80: 'TC_03.036', 81: 'TC_03.037', 82: 'TC_03.038',
    83: 'TC_03.039 (màn là trang: sau Lưu nháp chuyển về danh sách)', 84: 'TC_03.040', 85: 'TC_03.041',
    86: 'TC_03.042, TC_03.008', 87: 'TC_03.014, TC_03.043', 88: 'TC_03.044, TC_03.016', 89: 'TC_03.045',
    90: 'TC_03.046 (màn là trang: sau Gửi duyệt chuyển về danh sách)', 91: 'TC_03.047', 92: 'TC_03.048',
    93: 'TC_03.049', 94: 'TC_03.050',
    95: 'TC_03.051 (màn là trang, không có nút X — kiểm rời màn bằng menu, đóng tab, F5)',
    96: 'TC_03.052', 97: 'TC_03.053', 98: 'TC_03.054', 99: 'TC_03.055', 100: 'TC_03.056',
    101: 'TC_03.057', 102: 'TC_03.058',
    # IV. Chỉnh sửa
    103: 'TC_04.001 (màn Sửa là trang, không phải popup)', 104: 'TC_04.002', 105: 'TC_04.003', 106: 'TC_04.004',
    107: 'TC_04.005', 108: 'TC_04.006', 109: 'TC_04.007', 110: 'TC_04.008', 111: 'TC_04.009', 112: 'TC_04.010, TC_04.011',
    113: 'TC_04.012', 114: 'TC_04.013', 115: 'TC_04.014 (giới hạn có thật là dung lượng file 20MB)',
    116: 'TC_04.015, TC_04.016', 117: 'TC_04.017', 118: 'TC_04.018',
    119: 'TC_04.019', 120: 'TC_04.020', 121: 'TC_04.021', 122: 'TC_04.022', 123: 'TC_04.023', 124: 'TC_04.024', 125: 'TC_04.025',
    126: 'N/A: màn không có trạng thái Khóa; trường hợp gần nhất (phiếu đã gửi duyệt không sửa được) kiểm ở TC_04.026',
    127: 'TC_04.027 (lệch: thông báo là câu tiếng Anh "Item Not Found!" — đúng theo code)',
    128: 'TC_04.028 (chỉ người lập sửa được nên kiểm 2 tab cùng tài khoản)',
    129: 'TC_04.029, TC_10.003',
    # V. Xóa
    130: 'TC_05.001', 131: 'TC_05.002', 132: 'TC_05.003', 133: 'TC_05.004', 134: 'TC_05.005', 135: 'TC_05.006',
    136: 'TC_05.007',
    137: 'N/A: màn không có trạng thái Khóa; phiếu không ở Đang tạo thì không xóa được (TC_05.006)',
    138: 'TC_05.008, TC_05.009 (lệch: phiếu đã bị xóa báo "Item Not Found!" và bảng không tự nạp lại — đúng theo code)',
    139: 'TC_05.004', 140: 'TC_05.004', 141: 'TC_05.011',
    # VI. Lịch sử thay đổi
    162: 'TC_06.001', 163: 'TC_06.002 (lịch sử dạng dòng thời gian: mỗi mốc có thời gian, hành động, người thực hiện, nội dung)',
    164: 'TC_06.003', 165: 'TC_06.004', 166: 'TC_06.005', 167: 'TC_06.006', 168: 'TC_06.007',
    169: 'TC_06.008', 170: 'TC_06.009', 171: 'TC_06.010', 172: 'TC_06.011', 173: 'TC_06.011', 174: 'TC_06.012', 175: 'TC_06.013',
    176: 'TC_06.014', 177: 'TC_06.015', 178: 'TC_06.016, TC_06.019',
    179: NA_LOCK, 180: NA_LOCK, 181: NA_IMPORT,
    182: 'TC_06.017', 183: 'TC_06.018', 184: 'TC_06.021', 185: 'TC_06.022',
    # VII. Xem chi tiết
    186: 'TC_07.001 (màn chi tiết là trang, không phải popup)', 187: 'TC_07.002', 188: 'TC_07.003, TC_07.004',
    189: 'TC_07.005', 190: 'TC_07.006', 191: 'TC_07.007', 192: 'TC_07.008', 193: 'TC_07.009',
    194: 'N/A: màn không có trạng thái Khóa; phiếu Đã duyệt (trạng thái cuối, chỉ xem) kiểm ở TC_07.010',
    195: 'TC_07.011',
    196: 'TC_07.013 (màn chi tiết là trang: "đóng" là nút Quay lại)',
    197: 'TC_07.013 (lệch: quay lại giữ bộ lọc, sắp xếp nhưng về trang 1 — đúng theo code)',
    # VIII. Tùy chỉnh cột
    198: 'TC_08.001', 199: 'TC_08.002', 200: 'TC_08.003', 201: 'TC_08.004', 202: 'TC_08.005', 203: 'TC_08.006',
    204: 'TC_08.007', 205: 'TC_08.008', 206: 'TC_08.004, TC_08.005', 207: 'TC_08.010', 208: 'TC_08.011', 209: 'TC_08.012',
    210: 'TC_08.013', 211: 'TC_08.014',
    # IX. Xuất Excel
    212: 'TC_09.001', 213: 'TC_09.002', 214: 'TC_09.003', 215: 'TC_09.004', 216: 'TC_09.005', 217: 'TC_09.006',
    218: 'TC_09.007', 219: 'TC_09.008', 220: 'TC_09.009, TC_09.021', 221: 'TC_09.010',
    222: 'TC_09.011', 223: 'TC_09.012', 224: 'TC_09.013', 225: 'TC_09.014', 226: 'TC_09.015', 227: 'TC_09.016',
    228: 'TC_09.017', 229: 'TC_09.018', 230: 'TC_09.019',
    # X. Ảnh hưởng các màn hình sử dụng dữ liệu
    268: 'TC_10.001', 269: 'TC_10.002', 270: 'TC_10.003, TC_05.006', 271: NA_LOCK, 272: 'TC_10.004', 273: NA_LOCK,
    274: 'TC_10.005', 275: NA_IMPORT, 276: NA_LOCK, 277: NA_LOCK,
    278: 'TC_10.006 (phiếu không có trường Tên — kiểm sửa Diễn giải đồng bộ danh sách / chi tiết / in / Excel)',
    279: 'TC_10.007 (số phiếu tự sinh, không sửa được — kiểm liên kết với phiếu kế toán giữ nguyên)',
    280: 'TC_10.008', 281: 'TC_10.009, TC_10.010', 282: 'TC_10.011', 283: 'TC_10.012', 284: 'TC_10.013', 285: 'TC_10.014',
    286: 'TC_10.015, TC_10.016 (lệch: không chặn dùng lại cùng phiếu xác nhận bảo hành ở nhiều phiếu — đúng theo code, giống ERP)',
    # XI. Phân quyền
    287: 'TC_11.001, TC_11.002, TC_11.003, TC_11.004, TC_11.006, TC_11.007',
    288: 'TC_11.013, TC_11.011', 289: 'TC_11.014 (lập phiếu không gắn quyền riêng)',
    290: 'TC_11.010, TC_11.015', 291: 'TC_11.010, TC_11.015', 292: NA_LOCK,
    293: 'TC_11.016 (không có Import; Xuất Excel không gắn quyền riêng, xuất trong phạm vi xem)',
    294: 'TC_11.017', 295: 'TC_11.018, TC_11.010', 296: 'TC_11.019, TC_11.020, TC_11.011', 297: 'TC_11.021',
    298: 'TC_11.022', 299: 'TC_11.002, TC_11.003, TC_11.004, TC_11.005, TC_11.023',
    # XII. Duyệt phiếu = Lập phiếu kế toán
    300: 'TC_12.001, TC_11.008, TC_11.009 (màn không có nút "Duyệt": kế toán duyệt bằng Lập phiếu kế toán)',
    301: 'TC_12.002 (lệch: bấm Lập phiếu kế toán không có hộp xác nhận; hộp "Xác nhận duyệt phiếu kế toán" ở bước Lưu và duyệt)',
    302: 'TC_12.003', 303: 'TC_12.004', 304: 'TC_12.005, TC_10.015', 305: 'TC_12.006', 306: 'TC_12.007', 307: 'TC_12.008',
    308: 'TC_12.009', 309: 'TC_12.010', 310: 'TC_12.011', 311: 'TC_12.012',
    312: 'TC_12.013 (lệch: lịch sử phiếu yêu cầu không ghi mốc Đang duyệt / Đã duyệt; Người duyệt, Ngày duyệt có trên phiếu)',
    # XIII. Không duyệt phiếu = Từ chối
    313: 'TC_13.001 (tên nghiệp vụ trên màn: Từ chối)', 314: 'TC_13.002', 315: 'TC_13.003', 316: 'TC_13.004',
    317: 'TC_13.005 (lệch: lý do quá 1.000 ký tự thì báo lỗi rồi cửa sổ tự đóng, mất nội dung đã nhập — đúng theo code)',
    318: 'TC_13.006', 319: 'TC_13.007', 320: 'TC_13.008', 321: 'TC_13.009', 322: 'TC_13.010', 323: 'TC_13.011', 324: 'TC_13.012',
}
for _stt in range(142, 162):          # Khóa / Mở khóa
    TC_MAP[_stt] = NA_LOCK
for _stt in range(231, 268):          # Import Excel
    TC_MAP[_stt] = NA_IMPORT

SRS_INTRO = '2.1.1; 2.2.1; 2.5.2; 2.7.2; 2.11.2; 2.15.1'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Khóa / Mở khóa — ghi rõ dưới ma trận)',
    14: 'Phần 2 (không có Import; In, Xuất Excel, Lịch sử không gắn quyền riêng)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.5.1; 2.7.1; 2.8.1; 2.9.1; 2.10.1; 2.11.1; 2.12.1; 2.13.1; 2.14.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.2.1; 2.4.1; 2.5.2; 2.7.2; 2.12.2; 2.14.2',
    23: '2.1.1; 2.2.1; 2.5.2; 2.15.1 (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.5.3; 2.11.3', 25: '2.1.2; 2.3.2; 2.9.3; 2.11.3; 2.13.3; 2.15.2',
    26: '2.1.3; 2.5.4', 27: '2.1.3; 2.5.4', 28: '2.1.3; 2.5.4', 29: '2.1.4; 2.5.5', 30: '2.1.4; 2.5.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3', 33: '2.1.1; 2.1.3; 2.4.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3', 37: '2.1.3',
    38: '2.1.1; 2.1.3', 39: '2.1.1', 40: '2.1.4',
    41: '2.2.1; 2.2.3', 42: '2.2.1', 43: '2.2.1; 2.2.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.2.3', 45: '2.2.3',
    46: '2.2.1', 47: '2.2.1; 2.2.4', 48: '2.2.3; 2.2.4', 49: '2.2.1; 2.2.3', 50: '2.1.3; 2.2.1', 51: '2.2.4',
    52: '2.5.2; 2.1.3', 53: '2.5.4', 54: '2.5.4', 55: '2.5.2; Phần 4 — BR-08, BR-11', 56: '2.5.4; 2.5.5', 57: '2.5.5',
    58: '2.5.4; 2.5.5', 59: '2.5.2 (màn Tạo là trang: không có (x) / click ngoài — ghi rõ cách rời màn)', 60: '2.5.2; 2.5.5',
    61: '2.5.2; 2.5.5', 62: '2.5.5',
    63: '2.7.2; 2.1.3', 64: '2.7.2; 2.7.5', 65: '2.7.2; 2.7.4', 66: '2.7.4; 2.7.5', 67: '2.7.2', 68: '2.7.2',
    69: '2.7.2; 2.7.5', 70: '2.7.2; 2.7.5', 71: '2.7.2 (không có Khóa; phiếu đã gửi duyệt coi như khóa sửa)', 72: '2.7.2; 2.15.1',
    73: '2.7.5',
    74: '2.9.2; 2.9.4', 75: '2.9.2', 76: '2.9.2', 77: '2.9.2 (không có Khóa)', 78: '2.9.3; 2.9.4', 79: '2.9.4',
    80: '2.9.2; 2.9.4', 81: '2.9.2', 82: '2.9.5',
    83: 'Phần 1; Phần 4 — BR-03 (không có Khóa / Mở khóa; 4 trạng thái phiếu mô tả ở Thuật ngữ và BR-03)',
    94: '2.15.1; 2.15.2', 95: '2.15.3', 96: '2.15.3', 97: '2.15.1; 2.15.3', 98: '2.15.1; 2.15.3', 99: '2.15.1',
    100: '2.15.1', 101: '2.15.4',
    120: '2.14.2; 2.14.3', 121: '2.14.4', 122: '2.14.2; 2.14.4', 123: '2.14.4', 124: '2.14.4; 2.14.5', 125: '2.14.2',
    126: '2.14.2', 127: '2.14.2', 128: '2.14.2; 2.14.4', 129: '2.14.5',
    130: '2.10.2', 131: '2.10.3', 132: '2.10.4', 133: '2.10.2; 2.10.4',
    134: 'N/A: màn không có trạng thái Khóa (phiếu Đang duyệt / Đã duyệt chỉ xem — ghi ở 2.10.2)',
    135: '2.10.4; 2.10.5', 136: '2.10.4; 2.15.3',
    137: '2.10.2 (lệch: quay lại giữ bộ lọc, sắp xếp nhưng về trang 1 — SRS ghi theo code)', 138: '2.10.5',
    139: '2.4.1; 2.4.2', 140: '2.4.3', 141: '2.4.1; 2.4.3', 142: '2.4.3; 2.4.4', 143: '2.4.1; 2.4.4', 144: '2.4.1',
    145: '2.4.1', 146: '2.4.4',
    147: 'Phần 4 — BR-11', 148: 'Phần 4 — BR-12',
    149: 'N/A: không có Khóa và không có trường nghiệp vụ duy nhất nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-13', 151: 'Phần 4 — BR-03, BR-14; 2.9.2',
    152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-14; Phần 5', 154: 'Phần 4 — BR-15', 155: 'Phần 4 — BR-01 đến BR-10',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5', 163: 'Phần 5',
}
for _stt in range(84, 94):            # FR-06 Khóa / Mở khóa
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
for _stt in range(102, 120):          # FR-08 Import Excel
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'

if __name__ == '__main__':
    write(HERE, TC_MAP, SRS_MAP)
