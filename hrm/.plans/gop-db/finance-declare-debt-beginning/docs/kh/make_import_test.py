# -*- coding: utf-8 -*-
"""Dựng file thử Import (chỉ để chụp Load lên bảng + Validate, KHÔNG bấm Import) từ file mẫu tải trên dev.
Dòng 1 hợp lệ (HĐ hãng chưa khai báo của 75TPHXCH-2), dòng 2 sai mọi cột, dòng 3 trùng dòng 1, dòng 4 quá hạn thiếu ngày BGNT."""
import os
import openpyxl
HERE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(HERE, 'hdsd_shots', 'template.xlsx')
wb = openpyxl.load_workbook(src)
ws = wb.active
rows = [
    ['75TPHXCH-2', 'HĐ_TPE_HN_KD3_26_0826_PO2610-1710', 'HDHNTDA', '1311', 'Dư nợ', '1500000', '1', ''],
    ['KHONG-CO', 'ABC-123', 'HDXX', '9999', 'Dư', '-5', '', ''],
    ['75TPHXCH-2', 'HĐ_TPE_HN_KD3_26_0826_PO2610-1710', 'HDHNTDA', '1311', 'Dư nợ', '2000000', '', ''],
    ['75TPHXCH-2', 'HĐ_TPE_HN_KD3_26_0805_HD2605-0006', 'HDHNTDA', '1311', 'Dư nợ', '3000000', '2', ''],
]
for i, r in enumerate(rows):
    for j, v in enumerate([i + 1] + r):
        ws.cell(row=2 + i, column=1 + j, value=v)
wb.save(os.path.join(HERE, 'hdsd_shots', 'import_test.xlsx'))
print('ok')
