# -*- coding: utf-8 -*-
"""Testcase #11643 — bản BỔ SUNG 27/11/2026 (user chốt: GIỮ NGUYÊN case cũ + kết quả test, chỉ sửa case lỗi thời và thêm case mới).

Nguồn:
  - Case cũ: `tab52_ban_cu_truoc_27-11.csv` (dump tab 52 trước khi sửa) — giữ nguyên 18 cột (ID, nội dung, Passed, ghi chú).
    3 case lỗi thời so với code 26/11 được sửa Expected, xoá KQ để test lại, ghi lý do ở cột Ghi chú.
  - Case mới: lấy theo tên từ `gen_testcase_11643_v2.py`, chỉ phần CHƯA có trong bản cũ; đánh số nối tiếp kiểu ID cũ
    (TC_<nhóm chuẩn>.<stt>: 03 Thêm, 04 Sửa, 05 Gửi duyệt, 06 Duyệt/Hủy duyệt, 07 Từ chối, 08 Hủy phiếu, 09 Lịch sử,
    10 Chi tiết, 15 Phân quyền).
Khuôn trình bày = tab "25. PPTT theo nhân viên" (mô tả 10 mục, summary, header 18 cột).
"""
import csv
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_testcase_11643_v2 as v2  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.worksheet.datavalidation import DataValidation  # noqa: E402

OUT = os.path.join(HERE, 'testcase - #11643 bổ sung 27-11.xlsx')
OLD_CSV = os.path.join(HERE, 'tab52_ban_cu_truoc_27-11.csv')
NOTE_UPD = 'Cập nhật 27/11 theo task sửa lại (%s) — cần test lại'

# ── case cũ ──
old_rows = list(csv.reader(open(OLD_CSV, encoding='utf-8')))
OLD = {r[2]: (r + [''] * 18)[:18] for r in old_rows if len(r) > 2 and r[2].startswith('TC_')}
assert len(OLD) == 19, len(OLD)


def old(tid):
    return list(OLD[tid])


def updated(tid, issue, **kw):
    r = old(tid)
    col = {'D': 3, 'G': 6, 'H': 7, 'I': 8}
    for k, v in kw.items():
        r[col[k]] = v
    r[9] = ''     # Actual Result
    r[10] = ''    # Status check lần 1
    r[11] = ''
    r[12] = NOTE_UPD % issue
    return r


r1 = old('TC_03.001')
s = 'Tầng 3: mỗi cặp có SL khách, Doanh số'
assert s in r1[8]
U_03_001 = updated('TC_03.001', '#12290', I=r1[8].replace(
    s, 'Tầng 3: mỗi cặp có "SL khách" và "Doanh số (VNĐ)", mỗi tiêu đề có biểu tượng ⓘ'))
r7 = old('TC_03.007')
U_03_007 = updated(
    'TC_03.007', '#12275',
    D='SL khách không có phần thập phân, Doanh số tối đa 2 số lẻ',
    G=r7[6].replace('3. Gõ 2.5 vào ô Doanh số.', '3. Gõ 2.5 vào ô SL khách.\n4. Gõ 1500000000.255 vào ô Doanh số (VNĐ).'),
    H='2.5\n1500000000.255',
    I='- Ô SL khách không nhận phần thập phân, chỉ chứa số nguyên\n'
      '- Ô Doanh số (VNĐ) nhận tối đa 2 chữ số thập phân: hiện 1,500,000,000.25, không gõ được chữ số thập phân thứ 3')
assert 'Doanh số (VNĐ)' in U_03_007[6]
U_10_001 = updated(
    'TC_10.001', '#12317',
    I='- Tiêu đề "Chi tiết phiếu giao chỉ tiêu kinh doanh theo phòng ban: TPE_CTKD_2027.00015" kèm nhãn Đang tạo\n'
      '- Khối "Thông tin phiếu" KHÔNG còn nhãn trạng thái riêng, KHÔNG còn dòng "Lý do từ chối" (lý do xem ở Lịch sử thay đổi)\n'
      '- Năm, Khối kinh doanh, Khu vực hiện dạng chữ trong KHUNG viền nền xám như ô bị khoá, không sửa được\n'
      '- Bảng không có ô nhập, không có thùng rác, liên kết Thêm / Chia\n'
      '- Thu / mở cây và ô Hiển thị đến cấp vẫn dùng được\n'
      '- Không có nút Lưu')

# ── case mới (lấy theo tên từ v2) ──
NEW = {tc[0]: tc for _, _, g in v2.GROUPS for tc in g}


def new(prefix, start, titles):
    out = []
    for i, t in enumerate(titles):
        fn, pr, pre, st, data, ex = NEW[t]
        out.append(['', '', 'TC_%s.%03d' % (prefix, start + i), fn, pr, pre, v2.steps(st), data or '', v2.exp(ex)]
                   + [''] * 9)
    return out


SEC = []
add_new_03 = ['Ô Năm chỉ có năm chưa có phiếu còn hiệu lực', 'Năm mặc định khi năm hiện tại đã có phiếu',
              'Bấm x ô Khối kinh doanh có số liệu — dropdown không đè hộp xác nhận', 'Bỏ khối: bấm Hủy thì giữ nguyên, bấm Bỏ khối thì xoá',
              'Bấm x ô Khu vực có số liệu — dropdown không đè hộp xác nhận', 'Tiêu đề cột có đơn vị và biểu tượng thông tin',
              'Phòng đã chia bộ phận thì số của phòng = tổng bộ phận']
grp3 = [t for t, *_ in v2.G3[2]]
grp5 = [t for t, *_ in v2.G5[2] if t != 'Màn Chi tiết hiện thống kê']
n = 13
SEC.append(('THÊM MỚI', 'Thêm mới',
            [U_03_001] + [old('TC_03.%03d' % i) for i in range(2, 7)] + [U_03_007] + [old('TC_03.%03d' % i) for i in range(8, 13)]
            + new('03', n, add_new_03)))
n += len(add_new_03)
SEC.append(('THÊM MỚI — CHỌN PHÒNG BAN / BỘ PHẬN THEO THỊ TRƯỜNG ĐÃ CHIA', 'Thêm mới — chọn phòng ban / bộ phận', new('03', n, grp3)))
n += len(grp3)
SEC.append(('THÊM MỚI — THỐNG KÊ DÒNG TỈNH/TP & TOÀN PHIẾU', 'Thêm mới — thống kê', new('03', n, grp5)))
SEC.append(('CHỈNH SỬA', 'Chỉnh sửa', [old('TC_04.001'), old('TC_04.002')] + new('04', 3, ['Ô Năm ở màn Sửa giữ năm của chính phiếu'])))
SEC.append(('GỬI DUYỆT', 'Gửi duyệt', new('05', 1, ['Lưu và gửi: có Doanh số mà thiếu SL khách', 'Lưu và gửi: có SL khách mà thiếu Doanh số',
                                                    'Lưu và gửi phiếu không có doanh số', 'Lưu và gửi thành công'])))
SEC.append(('DUYỆT / TỪ CHỐI / HỦY DUYỆT / HỦY PHIẾU', 'Duyệt / Từ chối / Hủy duyệt / Hủy phiếu',
            new('06', 1, ['Hủy duyệt bắt buộc nhập lý do', 'Lý do quá dài']) + new('07', 1, ['Từ chối ngay ở danh sách', 'Từ chối bỏ trống lý do'])
            + new('08', 1, ['Hủy phiếu bắt buộc nhập lý do'])))
SEC.append(('LỊCH SỬ THAY ĐỔI', 'Lịch sử thay đổi', new('09', 1, ['Lịch sử ghi rõ lý do từng thao tác', 'Lưu mà không sửa gì thì không ghi lịch sử',
                                                                  'Lịch sử Sửa chỉ ghi phần đổi'])))
SEC.append(('XEM CHI TIẾT PHIẾU', 'Xem chi tiết phiếu', [U_10_001, old('TC_10.002'), old('TC_10.010')] + new('10', 11, ['Màn Chi tiết hiện thống kê'])))
SEC.append(('IN PHIẾU', 'In phiếu', [old('TC_11.003')]))
SEC.append(('RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', 'Ràng buộc với các chức năng khác', [old('TC_14.001')]))
SEC.append(('PHÂN QUYỀN', 'Phân quyền', new('15', 1, ['Từ chối / Hủy duyệt chỉ hiện với người có quyền Duyệt'])))

ROMAN = v2.ROMAN


def build():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Trang tính1'
    TNR = v2.TNR
    for k, v in v2.WIDTHS.items():
        ws.column_dimensions[k].width = v
    wrap = Alignment(wrap_text=True, vertical='center')
    wrapc = Alignment(wrap_text=True, vertical='center', horizontal='center')
    fill = v2.fill

    ws['A1'] = 'MÔ TẢ CHỨC NĂNG'
    ws['A1'].font = Font(name=TNR, size=12, bold=True)
    ws.merge_cells('A1:I1')
    for i, (k, v) in enumerate(v2.DESC):
        r = 2 + i
        ws.cell(r, 1, k).font = Font(name=TNR, size=12, bold=True)
        ws.cell(r, 1).alignment = wrap
        ws.cell(r, 2, v).font = Font(name=TNR, size=12)
        ws.cell(r, 2).alignment = wrap
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=10)

    ws['A12'] = v2.TITLE
    ws['A12'].font = Font(name=TNR, size=15, bold=True, color='4A86E8')
    ws['A12'].alignment = wrapc
    ws.merge_cells('A12:E16')
    ws['F12'] = 'TEST SUMMARY'
    ws['F12'].font = Font(name=TNR, size=11, bold=True, color='FFFFFF')
    ws['F12'].alignment = wrapc
    for r in range(12, 18):
        for c in 'FGH':
            ws[f'{c}{r}'].fill = fill('4472C4')
    ws.merge_cells('F12:H17')
    L = 300
    dns = [('Số trường hợp DNS kiểm thử đạt (P):', f'=COUNTIFS(L20:L{L},"Passed")+COUNTIFS(K20:K{L},"Passed",L20:L{L},"")'),
           ('Số trường hợp DNS kiểm thử không đạt (F)', f'=COUNTIFS(L20:L{L},"Failed")+COUNTIFS(K20:K{L},"Failed",L20:L{L},"")'),
           ('Số trường hợp DNS kiểm thử đang xem xét (PE)', f'=COUNTIFS(L20:L{L},"Pending")+COUNTIFS(K20:K{L},"Pending",L20:L{L},"")'),
           ('Số trường hợp DNS kiểm thử chưa thực hiện', '=K17-K16'),
           ('Tổng số trường hợp DNS kiểm thử', '=SUM(K12:L14)'),
           ('Tổng số testcase', f'=COUNTIF(C20:C{L},"TC_*")')]
    tp = [('Số trường hợp TP kiểm thử đạt (P):', f'=COUNTIF(Q20:Q{L},"P")'),
          ('Số trường hợp TP kiểm thử không đạt (F)', f'=COUNTIF(Q20:Q{L},"F")'),
          ('Số trường hợp TP kiểm thử đang xem xét (PE)', f'=COUNTIF(Q20:Q{L},"PE")'),
          ('Số trường hợp TP kiểm thử chưa thực hiện', '=K17-P16'),
          ('Tổng số trường hợp TP đã kiểm thử', '=SUM(P12:Q14)')]
    for i, (lab, f) in enumerate(dns):
        r = 12 + i
        ws.cell(r, 9, lab).font = Font(name=TNR, size=11)
        ws.cell(r, 11, f).font = Font(name=TNR, size=11, bold=True)
        ws.cell(r, 9).alignment = wrap
        ws.cell(r, 11).alignment = wrapc
        for c in (9, 10, 11, 12):
            ws.cell(r, c).fill = fill('00FF00')
        ws.merge_cells(start_row=r, start_column=9, end_row=r, end_column=10)
        ws.merge_cells(start_row=r, start_column=11, end_row=r, end_column=12)
    for i, (lab, f) in enumerate(tp):
        r = 12 + i
        ws.cell(r, 13, lab).font = Font(name=TNR, size=11)
        ws.cell(r, 16, f).font = Font(name=TNR, size=11, bold=True)
        ws.cell(r, 13).alignment = wrap
        ws.cell(r, 16).alignment = wrapc
        ws.merge_cells(start_row=r, start_column=13, end_row=r, end_column=15)
        ws.merge_cells(start_row=r, start_column=16, end_row=r, end_column=17)
    ws.merge_cells('A18:I18')
    for c, h in enumerate(v2.HEAD, 1):
        cell = ws.cell(19, c, h)
        cell.font = Font(name=TNR, size=12, bold=True)
        cell.fill = fill('FF9900')
        cell.alignment = wrapc

    r = 20
    ids = []
    for gi, (gname, bname, rows) in enumerate(SEC):
        ws.cell(r, 3, '%s. %s' % (ROMAN[gi], gname))
        for c in range(1, 19):
            ws.cell(r, c).fill = fill('D6E4F0')
            ws.cell(r, c).font = Font(name=TNR, size=12, bold=True, color='1F4E79')
            ws.cell(r, c).alignment = Alignment(vertical='center')
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=13)
        r += 1
        first = r
        for row in rows:
            row = list(row)
            row[0] = v2.MODULE if r == first else None
            row[1] = bname if r == first else None
            ids.append(row[2])
            for c in range(1, 19):
                v = row[c - 1]
                cell = ws.cell(r, c, v if v not in ('',) else None)
                cell.font = Font(name=TNR, size=12)
                cell.alignment = wrapc if c in (3, 5, 11, 12, 17) else wrap
            ws.cell(r, 17, f'=IF(P{r}<>"",P{r},IF(O{r}<>"",O{r},IF(N{r}<>"",N{r},"")))')
            r += 1
        ws.merge_cells(start_row=first, start_column=1, end_row=r - 1, end_column=1)
        ws.merge_cells(start_row=first, start_column=2, end_row=r - 1, end_column=2)
    last = r - 1
    assert len(ids) == len(set(ids)), 'trùng TC ID'
    dv1 = DataValidation(type='list', formula1='"Passed,Failed,Pending,Not Executed"', allow_blank=True)
    dv2 = DataValidation(type='list', formula1='"P,F,PE"', allow_blank=True)
    ws.add_data_validation(dv1)
    ws.add_data_validation(dv2)
    dv1.add(f'K21:L{last}')
    dv2.add(f'N21:P{last}')
    wb.save(OUT)
    return ids, last


if __name__ == '__main__':
    ids, last = build()
    olds = [i for i in ids if i in OLD]
    print('Tổng %d case (cũ giữ %d, trong đó sửa 3: TC_03.001, TC_03.007, TC_10.001; mới %d), dòng cuối %d'
          % (len(ids), len(olds), len(ids) - len(olds), last))
    for gi, (g, _, rows) in enumerate(SEC):
        print('  %s. %s: %d' % (ROMAN[gi], g, len(rows)))
    print(OUT)
