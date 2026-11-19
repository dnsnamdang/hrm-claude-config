# -*- coding: utf-8 -*-
"""Dựng file thử Import (hdsd_shots/import_test.xlsx) từ file mẫu tải ở bước `capture.js template`:
giữ 2 dòng tiêu đề + gợi ý, thay dữ liệu bằng dòng đúng lẫn dòng lỗi để ảnh "sau Validate" thấy lý do lỗi.
Chỉ dùng Load lên bảng + Validate (không ghi dữ liệu). Chạy: python make_import_test.py
Kho / nhà / dãy có thật trên dev: EG_LN > N1 > D1 (dãy D1 đã có khoang K1)."""
import os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [  # STT, Mã kho, Mã nhà kho, Mã dãy, Mã khoang, Tên khoang, Trạng thái, Mô tả
    [1, 'EG_LN', 'N1', 'D1', 'DOC-K01', 'Khoang tài liệu 01', 'Hoạt động', ''],
    [2, 'EG_LN', 'N1', 'D1', 'DOC-K02', 'Khoang tài liệu 02', '', ''],
    [3, 'EG_LN', 'N1', 'D1', 'K1', 'Khoang tài liệu 03', 'Hoạt động', ''],
    [4, 'EG_LN', 'N99', '', 'Khoang @04', '', 'Tạm dừng', ''],
    [5, 'EG_LN', 'N1', 'D1', 'DOC-K01', 'Khoang tài liệu 05', 'Hoạt động', ''],
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
