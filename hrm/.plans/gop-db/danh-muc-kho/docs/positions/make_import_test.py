# -*- coding: utf-8 -*-
"""Dựng file thử Import (hdsd_shots/import_test.xlsx) từ file mẫu tải ở bước `capture.js template`:
giữ 2 dòng tiêu đề + gợi ý, thay dữ liệu bằng dòng đúng lẫn dòng lỗi để ảnh "sau Validate" thấy lý do lỗi.
Chỉ dùng Load lên bảng + Validate (không ghi dữ liệu). Chạy: python make_import_test.py
Mã kho / nhà / dãy / khoang lấy từ dữ liệu dev (EG_LN > N1 > D5 > K4, có sẵn vị trí EG_LN-N1-D5-K4-T5)."""
import os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [  # STT, Loại vị trí, Mã kho, Mã nhà kho, Mã dãy, Mã khoang, Mã vị trí, Tên vị trí, Trạng thái, Mô tả
    [1, 'Thuộc khoang', 'EG_LN', 'N1', 'D5', 'K4', 'DOC-VT01', 'Tầng tài liệu 01', 'Hoạt động', ''],
    [2, 'Tự do', 'EG_LN', '', '', '', 'DOC-VT-TD01', 'Vị trí tự do tài liệu 01', '', ''],
    [3, 'Thuộc khoang', 'EG_LN', 'N1', 'D5', 'K4', 'EG_LN-N1-D5-K4-T5', 'Tầng tài liệu 03', 'Hoạt động', ''],
    [4, 'Kệ', 'EG_LN', '', '', '', 'VT @04', '', 'Tạm dừng', ''],
    [5, 'Thuộc khoang', 'EG_LN', 'N99', '', '', 'DOC-VT05', 'Tầng tài liệu 05', 'Hoạt động', ''],
    [6, 'Thuộc khoang', 'EG_LN', 'N1', 'D5', 'K4', 'DOC-VT01', 'Tầng tài liệu 06', 'Hoạt động', ''],
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
