# -*- coding: utf-8 -*-
"""Dựng file thử Import (chỉ để chụp Load lên bảng + Validate, KHÔNG bấm Import) từ file mẫu tải trên dev.
Dòng 1: hàng đã khai tồn đầu tại kho PTT của TPE; dòng 2 sai mọi cột; dòng 3 thiếu cột + SL 0; dòng 4 kho không thuộc công ty."""
import os
import openpyxl
HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'hdsd_shots', 'template.xlsx'))
ws = wb.active
for r in ws.iter_rows(max_row=3, values_only=True):
    print(r)
rows = [
    ['Hệ thống rô bốt sấy hồng ngoại sóng ngắn 54kw, 2x 9 bóng', 'BLNS-IR-EVOPYRO', 'Bộ', 'PTT', 'N1-T2-KV', 10, 'TPE'],
    ['Hàng thử', 'KHONG-CO', 'XYZ', 'KXX', 'VT-XX', -5, 'ABC'],
    ['', '2Q-GSAQ', '', 'LN', '', 0, 'TPE'],
    ['Giá để sạc ắc quy', '2Q-GSAQ', 'Cái', 'LN', 'DÃY TÔN', 10, 'EG'],
]
start = 3  # dòng 1 tiêu đề, dòng 2 hướng dẫn; ghi đè dòng ví dụ (cột A = STT)
for i, r in enumerate(rows):
    for j, v in enumerate([i + 1] + r):
        ws.cell(row=start + i, column=1 + j, value=v)
wb.save(os.path.join(HERE, 'hdsd_shots', 'import_test.xlsx'))
print('ok')
