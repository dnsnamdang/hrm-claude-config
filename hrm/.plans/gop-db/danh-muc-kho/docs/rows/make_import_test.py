# -*- coding: utf-8 -*-
"""Dựng file thử Import (hdsd_shots/import_test.xlsx) từ file mẫu tải ở bước `capture.js template`:
giữ 2 dòng tiêu đề + gợi ý, thay dữ liệu bằng dòng đúng lẫn dòng lỗi để ảnh "sau Validate" thấy lý do lỗi.
Chỉ dùng Load lên bảng + Validate (không ghi dữ liệu). Chạy: python make_import_test.py
Dữ liệu dev 02/11/2026: kho DATD (Kho Dự án trọng điểm) > nhà N1 đã có dãy D1."""
import os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [  # STT, Mã kho, Mã nhà kho, Mã dãy, Tên dãy, Số khoang, Số vị trí mỗi khoang, Trạng thái, Mô tả
    [1, 'DATD', 'N1', 'DOC-D01', 'Dãy tài liệu 01', '2', '3', 'Hoạt động', ''],
    [2, 'DATD', 'N1', 'DOC-D02', 'Dãy tài liệu 02', '1', '2', '', ''],
    [3, 'DATD', 'N1', 'D1', 'Dãy tài liệu 03', '1', '1', 'Hoạt động', ''],
    [4, 'KHO_KHONG_CO', 'N1', 'Dãy @04', '', '0', '1', 'Tạm dừng', ''],
    [5, 'DATD', 'N1', 'DOC-D01', 'Dãy tài liệu 05', '101', '100', 'Hoạt động', ''],
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
