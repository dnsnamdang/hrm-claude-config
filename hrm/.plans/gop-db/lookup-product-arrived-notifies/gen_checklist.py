# -*- coding: utf-8 -*-
"""Đối chiếu tài liệu màn "Phiếu báo hàng về" với checklist "Mẫu tài liệu.xlsx" của tester (03/11/2026).

Chạy: python gen_checklist.py  -> "Đối chiếu checklist.xlsx" (chạy sau gen_testcase.py và gen_srs.py).
TC_MAP : stt checklist Testcase (1..324) -> TC ID trong testcase.xlsx, hoặc 'N/A: <lý do>'.
SRS_MAP: stt checklist SRS (1..163)      -> mục trong SRS (2.x / 2.x.y / Phần n), hoặc 'N/A: <lý do>'.
Ghi chú trong ngoặc (lệch so với checklist, cách hiểu riêng của màn) ra cột Ghi chú.
Màn chủ yếu CHỈ ĐỌC: không có Thêm mới, Chỉnh sửa, Khóa/Mở khóa, Lịch sử thay đổi, Import Excel, Duyệt, Không duyệt.
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

NA_CREATE = 'N/A: màn không có chức năng Thêm mới (phiếu báo hàng về được lập ở hệ thống ERP; TC_08.008 kiểm không có nút Tạo mới)'
NA_EDIT = 'N/A: màn không có chức năng Chỉnh sửa (mọi màn đều chỉ đọc)'
NA_LOCK = 'N/A: màn không có chức năng Khóa / Mở khóa (phiếu chỉ có 2 trạng thái Đã gửi, Đã yêu cầu nhập hàng)'
NA_HIS = 'N/A: màn không có chức năng Lịch sử thay đổi (TC_08.016 kiểm không có nút / khối Lịch sử)'
NA_IMPORT = 'N/A: màn không có chức năng Import Excel'
NA_APPROVE = 'N/A: màn không có chức năng Duyệt phiếu (trạng thái đổi khi lập yêu cầu nhập hàng / phân bổ chi phí — TC_07.002, TC_07.007)'
NA_REJECT = 'N/A: màn không có chức năng Không duyệt phiếu'

TC_MAP = {
    # I. Hiển thị danh sách và truy cập
    1: 'TC_01.001', 2: 'TC_01.002', 3: 'TC_01.003', 4: 'TC_01.004, TC_01.005', 5: 'TC_01.006 (màn không có cột mặc định ẩn)',
    6: 'TC_01.007, TC_01.008', 7: 'TC_01.009', 8: 'TC_01.010', 9: 'TC_01.011', 10: 'TC_01.001',
    11: 'TC_01.012', 12: 'TC_01.013', 13: 'TC_01.014', 14: 'TC_01.015', 15: 'TC_01.016', 16: 'TC_01.017',
    17: 'TC_01.018', 18: 'TC_01.012', 19: 'TC_01.001', 20: 'TC_01.019', 21: 'TC_01.019, TC_01.020',
    22: 'TC_01.020 (màn chỉ có Ngày tạo, không có cột Ngày cập nhật)', 23: 'TC_01.021', 24: 'TC_01.022', 25: 'TC_01.023',
    # II. Tìm kiếm và lọc
    26: 'TC_02.001', 27: 'TC_02.002', 28: 'TC_02.003',
    29: 'TC_02.004 (mã phiếu không có dấu nên kiểm ở ô Tên, mã hàng)', 30: 'TC_02.005',
    31: 'TC_02.006 (lệch: ký tự % và _ được hiểu là ký tự đại diện — gõ "%" ra toàn bộ phiếu; đúng theo code)',
    32: 'TC_02.007', 33: 'TC_02.037 (lệch: ô tìm nhanh không giới hạn số ký tự — đúng theo code)',
    34: 'TC_02.008', 35: 'TC_02.009', 36: 'TC_02.010',
    37: 'TC_02.011, TC_02.012, TC_02.013, TC_02.014, TC_02.015, TC_02.016, TC_02.017, TC_02.018, TC_02.019, TC_02.025',
    38: 'TC_02.035, TC_02.036', 39: 'TC_02.034', 40: 'TC_02.020', 41: 'TC_02.021', 42: 'TC_02.021', 43: 'TC_02.022',
    44: 'TC_02.023',
    45: 'TC_02.027, TC_02.028, TC_02.029, TC_02.033 (bộ lọc nhớ 10 phút mỗi khi đổi, sang màn khác rồi quay lại vẫn giữ — đúng theo code)',
    46: 'TC_02.030 (F5 trong 10 phút vẫn giữ bộ lọc và tab — đúng theo code)',
    47: 'TC_02.031',
    48: 'TC_02.032 (lệch: bộ lọc nhớ theo trình duyệt, không theo tài khoản — trong 10 phút tài khoản khác có thể thấy bộ lọc cũ; '
        'expected ghi theo yêu cầu, có dòng Lưu ý)',
    # V. Xóa
    130: 'TC_03.001', 131: 'TC_03.002',
    132: 'TC_03.003 (lệch: hộp xác nhận chỉ hỏi "Bạn có chắc muốn xóa bản ghi này không?", không ghi mã phiếu — đúng theo code)',
    133: 'TC_03.004', 134: 'TC_03.005', 135: 'TC_03.006, TC_07.004', 136: 'TC_03.007',
    137: 'N/A: màn không có trạng thái Khóa; phiếu đã lập yêu cầu nhập hàng không xóa được (TC_03.006)',
    138: 'TC_03.008', 139: 'TC_03.010', 140: 'TC_03.010, TC_03.004', 141: 'TC_03.011',
    # VII. Xem chi tiết
    186: 'TC_04.001 (màn chi tiết là trang, không phải popup)', 187: 'TC_04.002',
    188: 'TC_04.003, TC_04.004, TC_04.005', 189: 'TC_04.006', 190: 'TC_04.007', 191: 'TC_04.008', 192: 'TC_04.009',
    193: 'TC_04.010',
    194: 'N/A: màn không có trạng thái Khóa; phiếu Đã yêu cầu nhập hàng (trạng thái cuối, chỉ xem) kiểm ở TC_04.011',
    195: 'N/A: màn chi tiết không có khu vực Lịch sử (màn không ghi lịch sử thay đổi)',
    196: 'TC_04.014 (màn chi tiết là trang: "đóng" là nút Quay lại)',
    197: 'TC_04.014 (lệch: quay lại giữ bộ lọc, sắp xếp, đúng tab nhưng về trang 1 — đúng theo code)',
    # VIII. Tùy chỉnh cột
    198: 'TC_05.001', 199: 'TC_05.002', 200: 'TC_05.003', 201: 'TC_05.004', 202: 'TC_05.005', 203: 'TC_05.006',
    204: 'TC_05.007', 205: 'TC_05.008', 206: 'TC_05.004, TC_05.005', 207: 'TC_05.010', 208: 'TC_05.011', 209: 'TC_05.012',
    210: 'TC_05.013', 211: 'TC_05.014',
    # IX. Xuất Excel
    212: 'TC_06.001', 213: 'TC_06.002', 214: 'TC_06.003', 215: 'TC_06.004', 216: 'TC_06.005', 217: 'TC_06.006',
    218: 'TC_06.007', 219: 'TC_06.008', 220: 'TC_06.009', 221: 'TC_06.010',
    222: 'TC_06.011 (file rỗng có logo, tiêu đề, hàng tên cột, không có dòng "Không có dữ liệu")',
    223: 'TC_06.012', 224: 'TC_06.013', 225: 'TC_06.014', 226: 'TC_06.015', 227: 'TC_06.016', 228: 'TC_06.017',
    229: 'TC_06.018, TC_06.021 (danh sách không có cột số; ô số lượng kiểm ở file một phiếu)', 230: 'TC_06.019',
    # X. Ảnh hưởng các màn hình sử dụng dữ liệu
    268: 'N/A: màn không tạo phiếu (phiếu và dòng hàng lập ở hệ thống ERP)',
    269: 'N/A: màn không tạo phiếu (phiếu và dòng hàng lập ở hệ thống ERP)',
    270: 'TC_07.004, TC_03.006', 271: NA_LOCK,
    272: 'TC_07.010 (màn không sửa phiếu; kiểm liên kết giữ nguyên khi phiếu đổi trạng thái)', 273: NA_LOCK,
    274: 'TC_07.001', 275: NA_IMPORT, 276: NA_LOCK, 277: NA_LOCK,
    278: 'N/A: màn không sửa tên / nội dung phiếu', 279: 'N/A: mã phiếu do hệ thống ERP sinh, không sửa được trên màn',
    280: 'TC_07.006', 281: 'TC_07.002, TC_07.007', 282: 'TC_07.005', 283: 'TC_07.009', 284: 'TC_07.010', 285: 'TC_07.011',
    286: 'TC_07.012, TC_07.003',
    # XI. Phân quyền
    287: 'TC_08.001, TC_08.002, TC_08.003, TC_08.004, TC_08.006', 288: 'TC_08.007',
    289: 'TC_08.008 (màn không có Thêm mới — kiểm không có nút)', 290: NA_EDIT, 291: 'TC_08.009, TC_08.013',
    292: NA_LOCK, 293: 'TC_08.010, TC_08.011 (không có Import; Xuất Excel không gắn quyền riêng, xuất trong phạm vi xem)',
    294: 'TC_08.016 (màn không có Lịch sử thay đổi — kiểm không có nút)', 295: 'TC_08.012, TC_08.009', 296: 'TC_08.007',
    297: 'TC_08.013, TC_08.011', 298: 'TC_08.014', 299: 'TC_08.001, TC_08.002, TC_08.003, TC_08.004, TC_08.005, TC_08.015',
}
for _stt in range(49, 103):           # Thêm mới
    TC_MAP[_stt] = NA_CREATE
for _stt in range(103, 130):          # Chỉnh sửa
    TC_MAP[_stt] = NA_EDIT
for _stt in range(142, 162):          # Khóa / Mở khóa
    TC_MAP[_stt] = NA_LOCK
for _stt in range(162, 186):          # Lịch sử thay đổi
    TC_MAP[_stt] = NA_HIS
for _stt in range(231, 268):          # Import Excel
    TC_MAP[_stt] = NA_IMPORT
for _stt in range(300, 313):          # Duyệt phiếu
    TC_MAP[_stt] = NA_APPROVE
for _stt in range(313, 325):          # Không duyệt phiếu
    TC_MAP[_stt] = NA_REJECT

SRS_INTRO = '2.1.1; 2.4.1; 2.7.2; 2.11.2; 2.15.2'
SRS_MAP = {
    1: 'Phần 1', 2: 'Phần 1', 3: 'Phần 1', 4: 'Phần 1', 5: 'Phần 1', 6: 'Phần 1', 7: 'Phần 1', 8: 'Phần 1',
    9: 'Phần 2', 10: 'Phần 2', 11: 'Phần 2', 12: 'Phần 2',
    13: 'Phần 2 (màn không có Thêm, Sửa, Khóa / Mở khóa — ghi rõ dưới ma trận)',
    14: 'Phần 2 (không có Import, Lịch sử; Xuất Excel, In không gắn quyền riêng)',
    15: 'Phần 2', 16: 'Phần 2',
    17: 'Phần 3; 2.7.1; 2.8.1; 2.9.1; 2.10.1; 2.11.1; 2.12.1; 2.13.1; 2.14.1; 2.15.1',
    18: SRS_INTRO, 19: SRS_INTRO, 20: SRS_INTRO, 21: SRS_INTRO,
    22: '2.1.1; 2.4.1; 2.7.2; 2.11.2; 2.13.2',
    23: '2.1.1; 2.4.1; 2.11.2 (đoạn "Quy tắc chung" có liên kết đầu mỗi mục Giới thiệu)',
    24: '2.1.2; 2.7.3; 2.11.3', 25: '2.1.2; 2.5.2; 2.9.3; 2.11.3; 2.12.3',
    26: '2.1.3; 2.7.4', 27: '2.1.3; 2.7.4', 28: '2.1.3; 2.7.4', 29: '2.1.4; 2.11.5', 30: '2.1.4; 2.11.5',
    31: '2.1.1; 2.1.2', 32: '2.1.3; 2.2.3; 2.3.3', 33: '2.1.1; 2.1.3; 2.6.1', 34: '2.1.3', 35: '2.1.3; 2.1.4', 36: '2.1.3',
    37: '2.1.3', 38: '2.1.1; 2.2.1; 2.1.3', 39: '2.1.1; 2.1.3', 40: '2.1.4',
    41: '2.4.1; 2.4.3', 42: '2.4.1', 43: '2.4.1; 2.4.3 (không giới hạn số ký tự — đúng theo code)', 44: '2.4.3', 45: '2.4.3',
    46: '2.4.1', 47: '2.4.1; 2.4.4', 48: '2.4.3; 2.4.4', 49: '2.4.1; 2.4.3', 50: '2.1.3; 2.4.1', 51: '2.4.4',
    74: '2.11.2; 2.11.4', 75: '2.11.2', 76: '2.11.2', 77: 'N/A: màn không có trạng thái Khóa', 78: '2.11.3; 2.11.4',
    79: '2.11.4', 80: '2.11.2; 2.11.4', 81: '2.11.2', 82: '2.11.5',
    83: 'Phần 1; Phần 4 — BR-03 (không có Khóa / Mở khóa; 2 trạng thái phiếu mô tả ở Thuật ngữ và BR-03)',
    120: '2.7.2; 2.7.3', 121: '2.7.4', 122: '2.7.2; 2.7.4', 123: '2.7.4', 124: '2.7.4; 2.7.5', 125: '2.7.2', 126: '2.7.2',
    127: '2.7.2; 2.13.2', 128: '2.7.2; 2.7.4', 129: '2.7.5',
    130: '2.8.2; 2.9.2; 2.10.2', 131: '2.8.3; 2.9.3; 2.10.3', 132: '2.8.4; 2.9.4; 2.10.4', 133: '2.8.2; 2.8.4',
    134: 'N/A: màn không có trạng thái Khóa (phiếu Đã yêu cầu nhập hàng chỉ xem — ghi ở 2.8.4)',
    135: 'N/A: màn chi tiết không có khối Lịch sử (Phần 4 — BR-14)',
    136: 'N/A: màn chi tiết không có khối Lịch sử (Phần 4 — BR-14)',
    137: '2.8.2 (lệch: quay lại giữ bộ lọc, sắp xếp nhưng về trang 1 — SRS ghi theo code)', 138: '2.8.5; 2.9.5; 2.10.5',
    139: '2.6.1; 2.6.2', 140: '2.6.3', 141: '2.6.1; 2.6.3', 142: '2.6.3; 2.6.4', 143: '2.6.1; 2.6.4', 144: '2.6.1',
    145: '2.6.1', 146: '2.6.4',
    147: 'Phần 4 — BR-11', 148: 'Phần 4 — BR-12',
    149: 'N/A: không có Khóa và không nhập dữ liệu trên màn nên không có trường hợp trùng với bản ghi đã khóa',
    150: 'Phần 4 — BR-13, BR-05', 151: 'Phần 4 — BR-04, BR-05; 2.11.2',
    152: 'N/A: màn không có chức năng Khóa / Mở khóa',
    153: 'Phần 4 — BR-09; Phần 5', 154: 'Phần 4 — BR-14', 155: 'Phần 4 — BR-01 đến BR-15',
    156: 'Phần 5', 157: 'Phần 5', 158: 'Phần 5', 159: 'Phần 5', 160: 'Phần 5',
    161: 'N/A: màn không có chức năng Khóa / Mở khóa (Phần 5 theo khuôn Drive 4 cột STT | Nhóm | Màn hình | Đường dẫn)',
    162: 'Phần 5', 163: 'Phần 5 (quan hệ chứng từ nguồn – chứng từ dùng lại ghi trong cột Màn hình)',
}
for _stt in range(52, 63):            # FR-03 Thêm mới
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Thêm mới (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
for _stt in range(63, 74):            # FR-04 Chỉnh sửa
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Chỉnh sửa (ghi rõ ở Phần 1 Phạm vi chức năng)'
for _stt in range(84, 94):            # FR-06 Khóa / Mở khóa
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Khóa / Mở khóa (ghi rõ ở Phần 1 Phạm vi chức năng và dưới ma trận Phần 2)'
for _stt in range(94, 102):           # FR-07 Lịch sử
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Lịch sử thay đổi (Phần 1, Phần 4 — BR-14)'
for _stt in range(102, 120):          # FR-08 Import Excel
    SRS_MAP[_stt] = 'N/A: màn không có chức năng Import Excel (ghi rõ ở Phần 1 Phạm vi chức năng)'

if __name__ == '__main__':
    write(HERE, TC_MAP, SRS_MAP)
