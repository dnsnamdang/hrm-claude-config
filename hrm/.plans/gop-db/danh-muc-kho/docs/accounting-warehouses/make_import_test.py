# -*- coding: utf-8 -*-
"""Dựng file thử Import (hdsd_shots/import_test.xlsx) từ file mẫu tải ở bước `capture.js template` (khuôn màn mẫu
docs/warehouses): giữ 2 dòng tiêu đề + gợi ý, thay dữ liệu bằng dòng đúng lẫn dòng lỗi để ảnh "sau Validate" thấy lý do.
Chỉ dùng Load lên bảng + Validate (không ghi dữ liệu). Chạy: python make_import_test.py"""
import os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [  # STT, Mã kho kế toán, Tên kho kế toán, Nhập xuất thẳng, Mã kho vật lý, Địa chỉ, Mã kế toán kho, Trạng thái, Mô tả
    [1, 'DOC-KKT01', 'Kho kế toán tài liệu mẫu 01', 'Không', 'EG_LN', 'Liên Ninh', '91711075', 'Hoạt động', ''],
    [2, 'DOC-KKT02', 'Kho kế toán tài liệu mẫu 02', 'Có', '', '', '91711075, 92311095', 'Hoạt động', ''],
    [3, 'EG_LN01', 'Kho kế toán tài liệu mẫu 03', 'Không', 'EG_LN', 'Liên Ninh', '91711075', '', ''],
    [4, 'Kho @04', '', 'Chưa rõ', 'KHO_KHONG_CO', '', 'NV_KHONG_CO', 'Tạm dừng', ''],
    [5, 'DOC-KKT01', 'Kho kế toán tài liệu mẫu 05', 'Có', '', '', '91711075', 'Hoạt động', ''],
]
wb = openpyxl.load_workbook(os.path.join(HERE, 'hdsd_shots', 'template.xlsx'))
ws = wb.active
for r in range(3, ws.max_row + 1):
    for c in range(1, ws.max_column + 1):
        ws.cell(r, c).value = None
for i, row in enumerate(ROWS):
    for j, v in enumerate(row):
        ws.cell(3 + i, 1 + j).value = v
wb.save(os.path.join(HERE, 'hdsd_shots', 'import_test.xlsx'))
print('OK import_test.xlsx', len(ROWS), 'dòng')
