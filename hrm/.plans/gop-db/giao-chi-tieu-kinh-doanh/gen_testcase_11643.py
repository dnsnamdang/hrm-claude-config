# -*- coding: utf-8 -*-
"""Testcase RIÊNG phần thay đổi của task #11643 — "Phiếu giao chỉ tiêu kinh doanh theo phòng ban: Bỏ phần chọn chi tiết
khách hàng >> Thay vào đó nhập trực tiếp SL và giá trị vào". Khuôn chuẩn build_chuan loai='phieu', chỉ giữ các nhóm có
liên quan (Thêm mới · Chỉnh sửa · Gửi duyệt · Xem chi tiết · In · Xuất Excel · Ràng buộc).

Lấy lại case đã viết ở gen_testcase_phong_ban.py (bản cả màn) theo tên + bổ sung vài case riêng của task.
Chạy: python gen_testcase_11643.py -> "testcase - #11643 Nhập trực tiếp SL và doanh số.xlsx".
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_testcase_phong_ban as g  # noqa: E402
from gen_testcase_phong_ban import build_chuan, check_no_dash_pre, Sec, PRE_NEW, TAO_KD, HN_OTO1, PRE_EDIT, SUA, OLD8, \
    PRE_LIST, MENU, CHECK  # noqa: E402

OUT = os.path.join(HERE, 'testcase - #11643 Nhập trực tiếp SL và doanh số.xlsx')


def pick(src, titles):
    by = {tc[1]: tc for tc in src}
    miss = [t for t in titles if t not in by]
    assert not miss, 'Không tìm thấy case: %s' % miss
    return [by[t] for t in titles]


def sec(idx, picked, extra=()):
    s = Sec(idx)
    s.raw(picked)
    for e in extra:
        s.add(*e)
    return s


S1 = sec(1, pick(g.S3, [
    'KHÔNG còn phần chọn chi tiết khách hàng',
    'Nhập thẳng SL khách và Doanh số',
]), [
    ('Nhập đủ 8 ô và kiểm 4 cột Tổng cộng', 'P0', PRE_NEW,
     TAO_KD + [HN_OTO1, 'Nhập Khách hãng: Hàng hóa SL 2 / DS 1000, Dịch vụ SL 3 / DS 2000.',
               'Nhập Khách khác: Hàng hóa SL 4 / DS 3000, Dịch vụ SL 5 / DS 4000.'],
     ['Khách hãng: HH 2 / 1000, DV 3 / 2000', 'Khách khác: HH 4 / 3000, DV 5 / 4000'],
     ['Tổng cộng của dòng: Hàng hóa SL 6 / Doanh số 4,000; Dịch vụ SL 8 / Doanh số 6,000.',
      '4 ô Tổng cộng chỉ đọc, không gõ được.']),
    ('Nhiều phòng trong 1 Tỉnh/TP cộng dồn', 'P0', PRE_NEW,
     TAO_KD + [HN_OTO1 + ' Nhập Khách hãng / Hàng hóa SL khách 4, Doanh số 15000000000.',
               'Bấm "+ Thêm Phòng Ban", chọn PHÒNG KINH DOANH THƯƠNG MẠI, nhập SL khách 2, Doanh số 1000000000.'], '—',
     ['Dòng Thành phố Hà Nội: SL khách 6, Doanh số 16,000,000,000; ghi "Thành phố Hà Nội (2 phòng)".',
      'Dòng TỔNG cộng đúng các số trên, ghi "… · 2 phòng · …".']),
    ('Xoá số trong ô về trống', 'P1', PRE_NEW,
     TAO_KD + [HN_OTO1 + ' Nhập Doanh số 1000.', 'Xoá hết chữ số trong ô Doanh số.'], '—',
     ['Ô trở về trống; Tỉnh/TP và TỔNG giảm về 0 (ô Tỉnh/TP để trống, dòng TỔNG hiện 0).']),
    ('Dòng Năm trước chỉ đọc', 'P1', [g.ACC_A, OLD8, g.NO2027], TAO_KD + ['Thử bấm vào ô số của dòng Năm trước ở Hà Nội.'], '—',
     ['Không gõ được; dòng Năm trước chỉ để đối chiếu.']),
] + [tuple(tc[1:]) for tc in []])
S1.raw(pick(g.S3, [
    'Ô số chỉ nhận số nguyên không âm',
    'Số quá 13 chữ số bị chặn',
    'Số đúng 13 chữ số lưu được',
    'Có số mà chưa chọn phòng thì bị chặn',
    'Lỗi biến mất khi sửa đúng',
    'Dòng trống bị bỏ khi lưu',
    'Lưu (nháp) thành công',
    'Lưu nháp không bắt cặp SL khách / Doanh số',
    'Lưu và gửi: có Doanh số mà thiếu SL khách',
    'Lưu và gửi: có SL khách mà thiếu Doanh số',
    'Lưu và gửi: phiếu không có doanh số',
    'Dòng Năm trước lấy từ phiếu năm trước đã duyệt',
    'Xoá dòng phòng có số',
    'Tab Tổng hợp',
]))

S2 = sec(2, pick(g.S4, [
    'Sửa số liệu và lưu',
    'Lưu nhiều lần không nhân đôi dòng',
    'Xoá hết số rồi Lưu và gửi',
    'Phiếu cũ có danh sách khách hàng mở Sửa được',
]), [
    ('Màn Sửa không còn phần chọn chi tiết khách hàng', 'P0', PRE_EDIT, SUA + ['Quan sát dòng PHÒNG THIẾT BỊ Ô TÔ 1.'], '—',
     ['Không có nút / liên kết "Thêm / Xem Khách Hàng", không có dòng "Khách hàng mới".',
      '8 ô số điền sẵn số đã lưu, sửa trực tiếp được.']),
])

S3 = sec(3, pick(g.S5, [
    'Gửi duyệt phiếu thiếu cặp SL khách / Doanh số',
    'Gửi duyệt phiếu không có doanh số',
]))

S4 = sec(4, pick(g.S10, [
    'Phiếu cũ có danh sách khách hàng hiển thị đủ số',
    'Ô số 0 để trống, dòng TỔNG hiện 0',
]), [
    ('Màn Chi tiết hiện số đã nhập, chỉ đọc', 'P0', [g.ACC_A, g.DRAFT], [MENU, 'Bấm số phiếu TPE_CTKD_2027.000NN.'], '—',
     ['PHÒNG THIẾT BỊ Ô TÔ 1: Khách hãng / Hàng hóa SL khách 4, Doanh số 15,000,000,000; ô không sửa được.',
      'Không có phần / nút xem chi tiết khách hàng.']),
])

S5 = sec(5, pick(g.S11, ['In phiếu', 'In phiếu có bộ phận và phiếu cũ nhiều Tỉnh/TP']), [
    ('Bản in không còn danh sách khách hàng', 'P1', [PRE_LIST, OLD8], [MENU, 'In TPE_CTKD_2026.00008.'], '—',
     ['Bản in chỉ có các cột SL khách / Doanh số theo Tỉnh/TP và phòng, không có danh sách khách hàng chi tiết.']),
])

S6 = sec(6, pick(g.S13, ['Xuất Excel 1 phiếu']), [
    ('File Excel 1 phiếu ghi đúng số đã nhập', 'P1', [g.ACC_A, g.DRAFT], [MENU, 'Ở dòng phiếu mở menu, bấm "Xuất Excel".'], '—',
     ['Sheet khối Kinh doanh: PHÒNG THIẾT BỊ Ô TÔ 1 SL khách 4, Doanh số 15,000,000,000 (ô số, có dấu phẩy ngăn nghìn).',
      'Không có sheet / cột danh sách khách hàng.']),
])

S7 = sec(7, pick(g.S14, [
    'Phiếu theo nhân viên nạp chỉ tiêu từ phiếu phòng ban đã duyệt',
    'Phòng ở 2 khối cùng Tỉnh/TP thì chỉ tiêu cộng dồn',
    'Báo cáo giao chỉ tiêu theo phòng ban đếm SL khách theo số đã nhập',
    'Màn tạo / sửa cũ không còn được dùng',
    'Phiếu duyệt năm nay thành Năm trước của năm sau',
]))

S8 = sec(8, pick(g.S15, [
    'Quyền Tạo không sửa được phiếu người khác',
    'Mở đường link màn Sửa phiếu người khác',
]))

SECTIONS = [
    ('I', 'THÊM MỚI', S1),
    ('II', 'CHỈNH SỬA', S2),
    ('III', 'GỬI DUYỆT', S3),
    ('IV', 'XEM CHI TIẾT PHIẾU GIAO CHỈ TIÊU', S4),
    ('V', 'IN PHIẾU', S5),
    ('VI', 'XUẤT DANH SÁCH EXCEL / XUẤT EXCEL PHIẾU', S6),
    ('VII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S7),
    ('VIII', 'PHÂN QUYỀN', S8),
]
for i, (_, _, s) in enumerate(SECTIONS):
    s.idx = i + 1
check_no_dash_pre(SECTIONS, [])

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Task #11643: ở Phiếu giao chỉ tiêu kinh doanh theo phòng ban, BỎ phần chọn chi tiết khách hàng (nút "Thêm / Xem Khách '
     'Hàng", dòng "Khách hàng mới") — người dùng NHẬP TRỰC TIẾP SL khách và Doanh số vào các ô số trên dòng phòng ban.\n'
     'File này chỉ kiểm phần thay đổi đó (và chỗ khác đọc số đã nhập), không kiểm lại toàn bộ màn.'),
    ('2. Đối tượng được tính / hiển thị',
     '- 8 ô nhập trên mỗi dòng phòng: Khách hãng (Hàng hóa: SL khách, Doanh số · Dịch vụ: SL khách, Doanh số) và Khách khác '
     '(4 ô tương tự).\n- 4 cột Tổng cộng (chỉ đọc) = Khách hãng + Khách khác.\n'
     '- Dòng Tỉnh/TP, dòng TỔNG, tab Tổng hợp cộng từ số đã nhập; dòng Năm trước chỉ đọc.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Không còn: nút "Thêm / Xem Khách Hàng", cửa sổ chọn khách hàng, dòng "Khách hàng mới" ở màn Tạo / Sửa / Chi tiết / In / '
     'Excel.\n- Dòng phòng để trống hoàn toàn (không chọn phòng, không số) bị bỏ khi lưu.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Không áp dụng — task không đổi bộ lọc. Dòng Năm trước lấy từ phiếu đã duyệt của năm liền '
                                        'trước, cùng công ty, cùng khối.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Phiếu > Khối kinh doanh (mỗi khối 1 tab + Tổng hợp) > Khu vực > Tỉnh/TP > Phòng ban (8 ô số nhập thẳng).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tỉnh/TP = tổng các phòng; TỔNG = tổng các Tỉnh/TP; Tổng cộng = Khách hãng + Khách khác.\n'
     '- Tab Tổng hợp: mỗi Tỉnh/TP = tổng các khối.\n'
     '- Báo cáo giao chỉ tiêu theo phòng ban: số khách hãng = tổng SL khách đã nhập (không đếm danh sách khách hàng nữa).\n'
     '- Phiếu theo nhân viên nạp chỉ tiêu phòng = tổng số đã nhập của phòng ở phiếu phòng ban đã duyệt.'),
    ('7. Phân quyền cấp',
     'Không áp dụng — task không đổi phân quyền. Người lập cần quyền "Tạo chỉ tiêu kinh doanh theo phòng ban", người duyệt '
     'cần "Duyệt chỉ tiêu kinh doanh theo phòng ban".'),
    ('8. Cách tính các ô thống kê',
     '- Ô Tổng cộng / Hàng hóa / SL khách = Khách hãng / Hàng hóa / SL khách + Khách khác / Hàng hóa / SL khách (tương tự 3 ô '
     'còn lại).\n- Dòng TỔNG ghi "x Tỉnh/TP · y phòng · z bộ phận".'),
    ('9. Ghi chú đọc bảng',
     '- Tài khoản: A (Tạo, công ty TPE), D (Duyệt, công ty TPE), V4 (Xem mức Tổng công ty).\n'
     '- Ô số chỉ nhận số nguyên từ 0 trở lên, tối đa 13 chữ số; hiển thị có dấu phẩy ngăn nghìn.\n'
     '- Ô bằng 0 ở dòng phòng / Tỉnh/TP để TRỐNG; dòng TỔNG hiện 0.\n'
     '- Lưu ý: Lưu (nháp) KHÔNG bắt cặp SL khách / Doanh số; chỉ khi gửi duyệt mới bắt. "Lưu và gửi" bị chặn thì phiếu KHÔNG '
     'được lưu.\n- Phiếu cũ (còn danh sách khách hàng từ hệ thống cũ) vẫn hiện đúng số đã chốt.\n'
     '- Số phiếu mẫu "TPE_CTKD_2027.000NN": NN là số hệ thống cấp khi lưu. Số liệu mẫu lấy DB local, QA dựng lại nếu khác.'),
]

if __name__ == '__main__':
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='#11643 Giao chỉ tiêu KD theo phòng ban - Nhập trực tiếp SL và doanh số - Cập nhật ngày 19/11/2026',
                module_name='Giao chỉ tiêu KD theo phòng ban', description_block=DESCRIPTION_BLOCK, sections=SECTIONS,
                loai='phieu')
    tcs = [tc for _, _, s in SECTIONS for tc in s]
    p0 = sum(1 for tc in tcs if tc[2] == 'P0')
    print('TC: %d, P0: %d (%.1f%%)' % (len(tcs), p0, 100.0 * p0 / len(tcs)))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))
