# -*- coding: utf-8 -*-
"""Kiểm 1 file testcase có đúng KHUÔN CHUẨN tab "13. DM quốc gia" không (xem TC_CHUAN.md).

    python check_tc.py <file.xlsx> danh_muc|phieu|bao_cao
In từng lỗi; trả về True/False khi gọi kiem().
"""
import re
import sys

from openpyxl import load_workbook

# Thứ tự nhóm chuẩn (theo tab Quốc gia + thứ tự nhóm trong checklist "Mẫu tài liệu.xlsx").
# Nhóm không áp dụng cho màn thì BỎ, nhưng các nhóm có mặt phải đúng thứ tự này.
THU_TU = {
    'danh_muc': ['HIỂN THỊ TRANG & TRUY CẬP', 'TÌM KIẾM & LỌC DANH SÁCH', 'THÊM MỚI', 'CHỈNH SỬA', 'XÓA',
                 'KHÓA / MỞ KHÓA', 'LỊCH SỬ THAY ĐỔI', 'XEM CHI TIẾT', 'TÙY CHỈNH CỘT', 'XUẤT DANH SÁCH EXCEL',
                 'IMPORT TỪ FILE EXCEL', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', 'PHÂN QUYỀN'],
    'phieu': ['HIỂN THỊ TRANG & TRUY CẬP', 'TÌM KIẾM & LỌC DANH SÁCH', 'THÊM MỚI', 'CHỈNH SỬA', 'XÓA',
              'KHÓA / MỞ KHÓA', 'GỬI DUYỆT', 'DUYỆT PHIẾU', 'KHÔNG DUYỆT PHIẾU', 'HỦY PHIẾU', 'LỊCH SỬ THAY ĐỔI',
              'XEM CHI TIẾT', 'IN PHIẾU', 'TÙY CHỈNH CỘT', 'XUẤT DANH SÁCH EXCEL', 'IMPORT TỪ FILE EXCEL',
              'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', 'PHÂN QUYỀN'],
    'bao_cao': ['HIỂN THỊ TRANG & TRUY CẬP', 'TÌM KIẾM & LỌC DANH SÁCH', 'SỐ LIỆU BÁO CÁO', 'XEM CHI TIẾT',
                'TÙY CHỈNH CỘT', 'XUẤT DANH SÁCH EXCEL', 'IN BÁO CÁO', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC',
                'PHÂN QUYỀN'],
}
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV",
         "XVI", "XVII", "XVIII", "XIX", "XX"]
CAM = [r'TC-ROLE', r'\bE2E\b', r'\bERP\b', r'\bAPI\b', r'Postman', r'gọi thẳng']
HEADERS = ["Module", "Nhóm chức năng", "TC ID", "Chức năng", "Priority", "Tiền điều kiện", "Bước thực hiện",
           "Test Data", "Expected Result (chi tiết)", "KQ thực tế", "DNS check lần 1", "DNS check lần 2",
           "DNS check lần 3", "Ghi chú", "TP check lần 1", "TP check lần 2", "TP check lần 3"]


def _nhom(title):
    t = re.sub(r'^[IVXL]+\.\s*', '', str(title)).strip().upper()
    return t


def kiem(path, loai):
    loi = []
    ws = load_workbook(path).worksheets[0]
    norm = lambda v: re.sub(r'\s+', '', str(v or '')).lower()
    if [norm(ws.cell(17, c).value) for c in range(1, 18)] != [norm(h) for h in HEADERS]:
        loi.append('Dòng 17 không đúng 17 tiêu đề cột chuẩn')
    if ws.cell(16, 9).value != 'Tổng số testcase':
        loi.append('Thiếu dòng 16 "Tổng số testcase"')
    order = THU_TU[loai]
    last_idx, sec_no, cur_group, n_case = -1, 0, None, 0
    seen_group_text = False
    for r in range(18, ws.max_row + 1):
        c = ws.cell(r, 3).value
        if not c:
            continue
        s = str(c).strip()
        if not s.startswith('TC'):
            sec_no += 1
            m = re.match(r'^([IVXL]+)\.\s', s)
            if not m or m.group(1) != ROMAN[sec_no - 1]:
                loi.append('Dòng %d: tiêu đề nhóm phải đánh số La Mã liên tục (%s.) — đang là "%s"' % (r, ROMAN[sec_no - 1], s))
            g = _nhom(s)
            idx = next((i for i, k in enumerate(order) if g == k or g.startswith(k)), None)
            if idx is None:
                loi.append('Dòng %d: nhóm "%s" không có trong khuôn chuẩn (%s)' % (r, g, loai))
            elif idx <= last_idx:
                loi.append('Dòng %d: nhóm "%s" sai thứ tự' % (r, g))
            else:
                last_idx = idx
            cur_group, seen_group_text = g, False
            continue
        n_case += 1
        if not re.match(r'^TC_%02d\.\d{3}$' % sec_no, s):
            loi.append('Dòng %d: mã "%s" phải dạng TC_%02d.NNN' % (r, s, sec_no))
        if seen_group_text and (ws.cell(r, 1).value or ws.cell(r, 2).value):
            loi.append('Dòng %d: cột Module / Nhóm chức năng chỉ ghi ở case đầu mỗi nhóm' % r)
        if not seen_group_text and not ws.cell(r, 2).value:
            loi.append('Dòng %d: case đầu nhóm phải ghi cột Nhóm chức năng' % r)
        seen_group_text = True
        if ws.cell(r, 5).value not in ('P0', 'P1', 'P2'):
            loi.append('Dòng %d: Priority phải là P0/P1/P2' % r)
        for col in (4, 7, 9):
            if not ws.cell(r, col).value:
                loi.append('Dòng %d: thiếu %s' % (r, HEADERS[col - 1]))
        for col in (10, 11, 12, 13):
            if ws.cell(r, col).value not in (None, ''):
                loi.append('Dòng %d: cột %s phải để trống (DNS tự điền)' % (r, HEADERS[col - 1]))
        txt = ' '.join(str(ws.cell(r, col).value or '') for col in range(4, 10))
        for p in CAM:
            if re.search(p, txt):
                loi.append('Dòng %d: có chữ cấm "%s"' % (r, p))
    if order[-1] == 'PHÂN QUYỀN' and last_idx != len(order) - 1 and loai != 'khong_quyen':
        loi.append('Thiếu nhóm PHÂN QUYỀN ở cuối (màn có gắn quyền)')
    for x in loi[:40]:
        print('  [LỖI]', x)
    if len(loi) > 40:
        print('  … còn %d lỗi' % (len(loi) - 40))
    print('%s: %d case, %d nhóm, %d lỗi' % (path.split('\\')[-1].split('/')[-1], n_case, sec_no, len(loi)))
    return not loi


if __name__ == '__main__':
    sys.exit(0 if kiem(sys.argv[1], sys.argv[2]) else 1)
