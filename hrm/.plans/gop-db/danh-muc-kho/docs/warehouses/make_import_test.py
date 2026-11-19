# -*- coding: utf-8 -*-
"""Dựng file thử Import (hdsd_shots/import_test.xlsx) từ file mẫu tải ở bước `capture.js template`:
giữ 2 dòng tiêu đề + gợi ý, thay dữ liệu bằng dòng đúng lẫn dòng lỗi để ảnh "sau Validate" thấy lý do lỗi.
Chỉ dùng Load lên bảng + Validate (không ghi dữ liệu). Chạy: python make_import_test.py"""
import os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [  # STT, Mã kho, Tên kho, Địa chỉ, Mã thủ kho, Số nhà kho, Trạng thái, Mô tả
    [1, 'DOC-KVL01', 'Kho tài liệu mẫu 01', 'Hà Nội', 'EG-103', '2', 'Hoạt động', ''],
    [2, 'DOC-KVL02', 'Kho tài liệu mẫu 02', 'Hà Nội', 'EG-103, 91711075', '1', 'Hoạt động', ''],
    [3, 'EG_LN', 'Kho tài liệu mẫu 03', 'Hà Nội', 'EG-103', '1', '', ''],
    [4, 'Kho @04', '', '', 'NV_KHONG_CO', '0', 'Tạm dừng', ''],
    [5, 'DOC-KVL01', 'Kho tài liệu mẫu 05', 'Hà Nội', 'EG-103', '1', 'Hoạt động', ''],
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
