# -*- coding: utf-8 -*-
"""Dựng file thử Import (chỉ để chụp Load lên bảng + Validate, KHÔNG bấm Import) từ file mẫu tải trên dev.
Dòng 1 hợp lệ (HĐ mua đầu kỳ chưa khai báo của NCC TCX), dòng 2 sai mọi cột, dòng 3 trùng dòng 1,
dòng 4 USD thiếu tỷ giá, dòng 5 hợp đồng đã khai báo."""
import os
import openpyxl
HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, 'hdsd_shots', 'template.xlsx')
wb = openpyxl.load_workbook(src)
ws = wb.active
ws.delete_rows(2, ws.max_row)
rows = [
    ['TCX', 'TPE-TCX/PLC TRAINING', 'HDMDK', '3311', 'VNĐ', '', 'Dư có', '1500000'],
    ['KHONG-CO', 'ABC-123', 'HDXX', '9999', 'XYZ', '', 'Dư', '-5'],
    ['TCX', 'TPE-TCX/PLC TRAINING', 'HDMDK', '3311', 'VNĐ', '', 'Dư có', '2000000'],
    ['TCX', '0624/TPE-TCX/VF AXLE GA', 'HDMNN', '3311', 'USD', '', 'Dư có', '1000.25'],
    ['TCX', '0624/TPE-TCX/ VF AXLE GA', 'HDMDK', '3311', 'USD', '25990', 'Dư có', '500'],
]
for i, r in enumerate(rows):
    for j, v in enumerate([i + 1] + r):
        ws.cell(row=2 + i, column=1 + j, value=v)
wb.save(os.path.join(HERE, 'hdsd_shots', 'import_test.xlsx'))
print('ok')
