# -*- coding: utf-8 -*-
"""Dựng file thử Import (hdsd_shots/import_test.xlsx) từ file mẫu tải ở bước `capture.js template`:
giữ 2 dòng tiêu đề + gợi ý, thay dữ liệu bằng dòng đúng lẫn dòng lỗi để ảnh "sau Validate" thấy lý do lỗi.
Chỉ dùng Load lên bảng + Validate (không ghi dữ liệu). Chạy: python make_import_test.py"""
import os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [  # STT, Thứ tự, Trạng thái
    [1, '9101', 'Hoạt động'],
    [2, '9102', ''],
    [3, '3', 'Hoạt động'],      # trùng kiện đang có trên dev (Kiện 3)
    [4, '0', 'Hoạt động'],      # không lớn hơn 0
    [5, '9103', 'Tạm dừng'],    # trạng thái sai
    [6, '9101', 'Khóa'],        # trùng dòng 1 trong file
    [7, '09104', 'Hoạt động'],  # số 0 ở đầu — kiểm hệ thống có nhận như "9104" không
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
