# -*- coding: utf-8 -*-
"""Testcase #11643 (Phiếu giao chỉ tiêu KD theo phòng ban) — BẢN CẬP NHẬT 27/11/2026 theo task đã sửa lại
(góp ý TPE Lệ 21/11 + lỗi con #12288 #12290 #12291 #12317 #12318, code develop 26/11).

Khuôn = tab "25. PPTT theo nhân viên" của file Drive "Testcase _ Luồng mới_ERP + HRM" (gid 1753135176):
  - Dòng 1-11: MÔ TẢ CHỨC NĂNG (10 mục, A nhãn đậm, B:J gộp)
  - Dòng 12-17: tiêu đề (A12:E16) + TEST SUMMARY (F12:H17) + khối DNS (I:J nhãn, K:L số) + khối TP (M:O nhãn, P:Q số)
  - Dòng 18 trống, dòng 19 header 18 cột (A..R), từ dòng 20: nhóm La Mã (C:M gộp) + case TC_001…
  - A Module + B Nhóm chức năng gộp dọc theo nhóm; Expected mỗi ý 1 dòng "-   "; Q = kết quả TPE gần nhất
Chạy: python gen_testcase_11643_v2.py -> "testcase - #11643 cập nhật 27-11.xlsx" (rồi đẩy lên Google Sheet tab 52).
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'testcase - #11643 cập nhật 27-11.xlsx')

MODULE = 'Phiếu giao chỉ tiêu kinh doanh theo phòng ban'
TITLE = 'Testcase _ 11643 Phiếu giao chỉ tiêu kinh doanh theo phòng ban'

# ───────────────────────── câu dùng chung ─────────────────────────
MENU = 'Vào phân hệ Bán hàng > Kế hoạch > Giao chỉ tiêu kinh doanh > Theo phòng ban.'
MENU_CD = 'Vào phân hệ Bán hàng > Phê Duyệt > Kế hoạch & chỉ tiêu > Giao chỉ tiêu chờ duyệt.'
TAO = [MENU, 'Bấm Tạo mới.']
TAO_HN = TAO + ['Chọn Năm 2027, Khối kinh doanh = Kinh doanh, Khu vực = Đồng bằng sông Hồng.']

Q_VIEW = '"Xem chỉ tiêu"'
Q_CREATE = '"Tạo chỉ tiêu kinh doanh theo phòng ban"'
Q_APPROVE = '"Duyệt chỉ tiêu kinh doanh theo phòng ban"'

ACC_A = 'Tài khoản A có quyền ' + Q_CREATE + ', đang làm việc ở công ty TPE.'
ACC_D = 'Tài khoản D có quyền ' + Q_APPROVE + ', đang làm việc ở công ty TPE.'
COV = ('Phiếu phân chia thị trường theo phòng ban ĐÃ DUYỆT của TPE (khối Kinh doanh): Thành phố Hà Nội chia cho '
       'PHÒNG KINH DOANH 1 (cả phòng) và PHÒNG KINH DOANH 2 (chỉ bộ phận Nhóm KD2-1); Thành phố Hải Phòng chia cho '
       'PHÒNG KINH DOANH 1; Tỉnh Bắc Ninh chưa chia cho phòng nào. Khối Kinh doanh còn PHÒNG QUẢN TRỊ THÔNG TIN '
       '(không được chia ở tỉnh nào). Hà Nội có 3 khu vực kinh doanh đang hoạt động (KV HN 1, KV HN 2, KV HN 3).')
NO2027 = 'Công ty TPE chưa có phiếu giao chỉ tiêu nào cho năm 2027.'
PRE_NEW = ACC_A + '\n' + COV + '\n' + NO2027
DRAFT = ('Phiếu P1 = TPE_CTKD_2027.000NN do A lập, Đang tạo: Năm 2027, khối Kinh doanh, khu vực Đồng bằng sông Hồng; '
         'Hà Nội: PHÒNG KINH DOANH 1 Khách hãng / Hàng hóa SL khách 5, Doanh số 1,500,000,000.')
PRE_EDIT = ACC_A + '\n' + COV + '\n' + DRAFT
SUA = [MENU, 'Ở dòng phiếu P1 bấm Sửa (biểu tượng bút chì).']
XEM = [MENU, 'Bấm số phiếu P1.']
PENDING = DRAFT.replace('Đang tạo', 'Chờ duyệt (A đã gửi duyệt)')
APPROVED = DRAFT.replace('Đang tạo', 'Đã duyệt (D đã duyệt)')


def L(*lines):
    """Ô nhiều ý → xuống dòng thật."""
    return '\n'.join(lines)


def steps(lst):
    return '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(lst))


def exp(lst):
    return '\n'.join('-   ' + s for s in lst)


# (chức năng, priority, tiền điều kiện, [bước], test data, [expected])
G1 = ('HIỂN THỊ & TRUY CẬP', 'Hiển thị & truy cập', [
    ('Mở màn từ menu', 'P0', ACC_A, [MENU], '',
     ['Mở màn "Danh sách phiếu giao chỉ tiêu kinh doanh theo phòng ban"',
      'Có nút Tạo mới, Xuất Excel, Cấu hình cột; cột Hành động có nút Sửa và menu ⋮']),
    ('Mở màn từ lối vào Giao chỉ tiêu chờ duyệt', 'P1', ACC_D + '\n' + 'Có 2 phiếu Chờ duyệt và 3 phiếu Đã duyệt của TPE.', [MENU_CD], '',
     ['Danh sách chỉ có 2 phiếu Chờ duyệt của công ty TPE',
      'Tài khoản không có quyền ' + Q_APPROVE + ' không thấy mục menu này']),
    ('Bấm số phiếu mở màn Chi tiết', 'P1', PRE_EDIT, XEM, '',
     ['Mở màn "Chi tiết phiếu giao chỉ tiêu kinh doanh theo phòng ban: TPE_CTKD_2027.000NN", trạng thái nằm ở tiêu đề màn',
      'Danh sách không còn nút Xem riêng; xem chi tiết bằng cách bấm số phiếu']),
])

G2 = ('TẠO PHIẾU — NĂM, KHỐI KINH DOANH, KHU VỰC', 'Tạo phiếu — Năm, Khối kinh doanh, Khu vực', [
    ('Giao diện màn Tạo mới', 'P0', PRE_NEW, TAO, '',
     ['Tiêu đề "Tạo phiếu giao chỉ tiêu kinh doanh theo phòng ban"',
      'Khối "Thông tin phiếu": Năm*, Khối kinh doanh* (chọn nhiều); không có ô Số phiếu',
      'Khối "Chi tiết" hiện "Chưa có dữ liệu" khi chưa chọn khối',
      'Chân trang: Lưu, Lưu và gửi, Quay lại']),
    ('Ô Năm chỉ có năm chưa có phiếu còn hiệu lực', 'P0',
     ACC_A + '\nCông ty TPE có: phiếu năm 2026 Đã duyệt, phiếu năm 2028 Chờ duyệt, phiếu năm 2029 Đang tạo, phiếu năm 2030 đã Hủy.',
     TAO + ['Mở ô Năm.'], '',
     ['Danh sách năm từ 2025 đến 2036, KHÔNG có Năm 2026, Năm 2028, Năm 2029 (đang có phiếu Đã duyệt / Chờ duyệt / Đang tạo)',
      'CÓ Năm 2030 (phiếu năm 2030 đã Hủy không tính là còn hiệu lực)']),
    ('Năm mặc định khi năm hiện tại đã có phiếu', 'P1',
     ACC_A + '\nCông ty TPE đã có phiếu năm 2026 (Đã duyệt), chưa có phiếu năm 2027.', TAO, '',
     ['Ô Năm tự chọn sẵn Năm 2027 (năm trống gần nhất tính từ năm hiện tại), không để Năm 2026']),
    ('Ô Năm ở màn Sửa giữ năm của chính phiếu', 'P1', PRE_EDIT + '\nTPE còn phiếu năm 2028 Chờ duyệt.', SUA + ['Mở ô Năm.'], '',
     ['Ô Năm hiện Năm 2027 (năm của chính phiếu P1)', 'Danh sách năm không có Năm 2028']),
    ('Hai người cùng tạo phiếu cùng năm', 'P1', PRE_NEW + '\nTài khoản A2 cũng có quyền ' + Q_CREATE + ' ở TPE.',
     ['A và A2 cùng mở màn Tạo mới, cùng chọn Năm 2027, nhập số liệu.', 'A bấm Lưu.', 'A2 bấm Lưu.'], '',
     ['A lưu thành công', 'A2 bị báo đỏ dưới ô Năm: "Công ty đã có phiếu TPE_CTKD_2027.000NN (Đang tạo) cho năm 2027", phiếu không được lưu']),
    ('Bấm x ô Khối kinh doanh có số liệu — dropdown không đè hộp xác nhận', 'P0', PRE_EDIT, SUA + ['Bấm dấu x ở chip Kinh doanh trong ô Khối kinh doanh.'], '',
     ['Hiện hộp "Bỏ khối kinh doanh": "Bỏ khối Kinh doanh? Số liệu đã nhập của khối sẽ mất.", 2 nút Hủy / Bỏ khối',
      'Danh sách thả xuống của ô Khối kinh doanh KHÔNG bung ra đè lên hộp xác nhận',
      'Trong lúc hộp đang hỏi, ô Khối kinh doanh vẫn hiện chip Kinh doanh (chưa mất giá trị)']),
    ('Bỏ khối: bấm Hủy thì giữ nguyên, bấm Bỏ khối thì xoá', 'P1', PRE_EDIT,
     SUA + ['Bấm x ở chip Kinh doanh, bấm Hủy.', 'Bấm x lần nữa, bấm Bỏ khối.'], '',
     ['Bước 2: ô vẫn có khối Kinh doanh, bảng và số liệu giữ nguyên',
      'Bước 3: khối Kinh doanh bị bỏ, tab Kinh doanh và số liệu biến mất']),
    ('Bấm x ô Khu vực có số liệu — dropdown không đè hộp xác nhận', 'P0', PRE_EDIT,
     SUA + ['Ở tab Kinh doanh, bấm x ở chip Đồng bằng sông Hồng trong ô Khu vực.', 'Bấm Hủy.'], '',
     ['Hiện hộp "Bỏ khu vực": "Bỏ vùng Đồng bằng sông Hồng? 1 Tỉnh/TP có số liệu sẽ bị xoá.", 2 nút Hủy / Bỏ vùng',
      'Danh sách thả xuống của ô Khu vực KHÔNG bung ra đè lên hộp; trong lúc hỏi ô vẫn hiện chip Đồng bằng sông Hồng',
      'Bấm Hủy: khu vực và số liệu Hà Nội giữ nguyên']),
])

G3 = ('CHỌN PHÒNG BAN / BỘ PHẬN THEO THỊ TRƯỜNG ĐÃ CHIA', 'Chọn phòng ban / bộ phận', [
    ('Ô Phòng ban chỉ có phòng được chia thị trường tại Tỉnh/TP', 'P0', PRE_NEW, TAO_HN + ['Ở Thành phố Hà Nội mở ô Chọn phòng ban.', 'Ở Thành phố Hải Phòng mở ô Chọn phòng ban.'], '',
     ['Hà Nội: chỉ có PHÒNG KINH DOANH 1, PHÒNG KINH DOANH 2',
      'Hải Phòng: chỉ có PHÒNG KINH DOANH 1',
      'KHÔNG có PHÒNG QUẢN TRỊ THÔNG TIN ở cả 2 tỉnh (phòng này không được chia thị trường tại tỉnh)']),
    ('Tỉnh/TP chưa chia thị trường cho phòng nào', 'P1', PRE_NEW, TAO_HN + ['Ở Tỉnh Bắc Ninh mở ô Chọn phòng ban.'], '',
     ['Ô Chọn phòng ban không có phòng nào để chọn',
      'Dòng Tỉnh Bắc Ninh hiện "0 phòng được chia" và "Đã phân 0/0 phòng" màu cam; không có link "+ Thêm Phòng Ban"']),
    ('Phòng đã chọn không còn hiện ở dòng khác cùng Tỉnh/TP', 'P1', PRE_NEW,
     TAO_HN + ['Hà Nội dòng 1 chọn PHÒNG KINH DOANH 1.', 'Bấm "+ Thêm Phòng Ban", mở ô Chọn phòng ban ở dòng 2.'], '',
     ['Dòng 2 chỉ còn PHÒNG KINH DOANH 2']),
    ('Hết phòng được chia thì ẩn "+ Thêm Phòng Ban"', 'P0', PRE_NEW,
     TAO_HN + ['Hà Nội dòng 1 chọn PHÒNG KINH DOANH 1.', 'Bấm "+ Thêm Phòng Ban", dòng 2 chọn PHÒNG KINH DOANH 2.', 'Xoá dòng 2 (thùng rác), bấm Xoá.'], '',
     ['Sau bước 3: Hà Nội có 2 dòng = 2 phòng được chia, KHÔNG còn link "+ Thêm Phòng Ban"',
      'Sau bước 4: link "+ Thêm Phòng Ban" hiện lại dưới dòng cuối']),
    ('Link Chia Bộ Phận nằm cùng hàng nút Xoá', 'P1', PRE_NEW, TAO_HN + ['Quan sát dòng phòng ở Hà Nội (chưa chọn phòng), rồi chọn PHÒNG KINH DOANH 1.'], '',
     ['Link "+ Chia Bộ Phận" nằm cùng hàng với ô Chọn phòng ban và nút thùng rác (không xuống dòng riêng), dòng thấp hơn trước',
      'Chưa chọn phòng: link mờ, rê chuột hiện "Chọn phòng trước", bấm không có tác dụng',
      'Chọn phòng xong: link bấm được; "+ Thêm Phòng Ban" vẫn nằm dưới dòng phòng cuối của tỉnh']),
    ('Phòng chỉ được chia theo bộ phận thì chỉ chọn được bộ phận đó', 'P0', PRE_NEW,
     TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 2, bấm "+ Chia Bộ Phận".', 'Mở ô Chọn bộ phận.'], '',
     ['Ô Chọn bộ phận chỉ có Nhóm KD2-1, KHÔNG có Nhóm KD2-2 (Nhóm KD2-2 không được chia thị trường tại Hà Nội)',
      'Chọn Nhóm KD2-1 xong thì link "+ Thêm Bộ Phận" mờ, rê chuột hiện "Đã chia hết bộ phận của phòng"']),
    ('Phòng được chia cả phòng thì chọn được mọi bộ phận', 'P2', PRE_NEW + '\nPHÒNG KINH DOANH 1 có 2 bộ phận Nhóm KD1-1, Nhóm KD1-2.',
     TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, bấm "+ Chia Bộ Phận", mở ô Chọn bộ phận.'], '',
     ['Ô Chọn bộ phận có đủ Nhóm KD1-1, Nhóm KD1-2']),
    ('Phòng không còn được chia thị trường thì báo lỗi khi lưu', 'P0',
     PRE_EDIT + '\nSau khi P1 lưu, phiếu phân chia thị trường giao Hà Nội cho PHÒNG KINH DOANH 1 bị Hủy duyệt.',
     SUA + ['Không sửa gì, bấm Lưu.'], '',
     ['Ô phòng vẫn hiện đúng tên PHÒNG KINH DOANH 1',
      'Báo đỏ ngay dưới ô phòng: "Phòng chưa được phân chia thị trường tại Tỉnh/TP này", phiếu không được lưu',
      'Chọn lại phòng hợp lệ thì lỗi đỏ mất, Lưu được']),
])

G4 = ('NHẬP SL KHÁCH / DOANH SỐ', 'Nhập SL khách / Doanh số', [
    ('Không còn phần chọn chi tiết khách hàng', 'P0', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1.'], '',
     ['Dòng phòng có 8 ô nhập thẳng: Khách hãng (Hàng hóa, Dịch vụ) và Khách khác (Hàng hóa, Dịch vụ), mỗi nhóm có SL khách và Doanh số',
      'KHÔNG có nút / cửa sổ "Thêm / Xem Khách Hàng", không có ô tích "Khách hàng mới"',
      'Nhóm Tổng cộng chỉ hiển thị, không gõ được']),
    ('Tiêu đề cột có đơn vị và biểu tượng thông tin', 'P0', PRE_NEW, TAO_HN + ['Quan sát hàng tiêu đề bảng.', 'Rê chuột vào biểu tượng ⓘ của cột Doanh số nhóm Khách hãng › Hàng hóa.'], '',
     ['Cột doanh số ghi "Doanh số (VNĐ)" ở cả 6 cặp cột; cột số khách ghi "SL khách"',
      'Mỗi tiêu đề SL khách / Doanh số (VNĐ) có biểu tượng ⓘ',
      'Rê chuột: tiêu đề "Doanh số — Khách hãng · Hàng hóa", giải thích Khách hãng = khách được tích "Là khách hãng" trong danh mục Khách hàng, Hàng hóa = chỉ tiêu bán hàng hóa, Doanh số đơn vị VNĐ']),
    ('Nhập số và cộng Tổng cộng, dòng Tỉnh/TP, dòng TỔNG', 'P0', PRE_NEW,
     TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, nhập theo Test Data.', 'Bấm "+ Thêm Phòng Ban", chọn PHÒNG KINH DOANH 2, nhập Khách hãng / Hàng hóa SL khách 2, Doanh số 500,000,000.'],
     L('PHÒNG KINH DOANH 1:', 'Khách hãng Hàng hóa: 5 / 1,500,000,000', 'Khách hãng Dịch vụ: 2 / 300,000,000', 'Khách khác Hàng hóa: 3 / 600,000,000'),
     ['Tổng cộng dòng PHÒNG KINH DOANH 1: Hàng hóa 8 / 2,100,000,000; Dịch vụ 2 / 300,000,000',
      'Dòng Thành phố Hà Nội: Khách hãng Hàng hóa 7 / 2,000,000,000; Khách khác Hàng hóa 3 / 600,000,000; Tổng cộng Hàng hóa 10 / 2,600,000,000, Dịch vụ 2 / 300,000,000',
      'Dòng TỔNG bằng tổng các Tỉnh/TP']),
    ('SL khách chỉ nhận số nguyên không âm', 'P1', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, gõ lần lượt vào ô SL khách.'], L('-5', 'abc', '2.5'),
     ['Không nhận dấu trừ, không nhận chữ', 'Không nhận phần thập phân, ô chỉ chứa số nguyên']),
    ('Doanh số nhận tối đa 2 chữ số thập phân', 'P1', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, nhập SL khách 1, gõ vào ô Doanh số (VNĐ).', 'Bấm Lưu.'], L('1500000000.25', '1500000000.255'),
     ['1500000000.25 hiện 1,500,000,000.25 và lưu được', 'Không gõ được chữ số thập phân thứ 3']),
    ('Số vượt 13 chữ số bị chặn', 'P0', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, ô SL khách 1, ô Doanh số gõ 14 chữ số.', 'Bấm Lưu.', 'Sửa thành 13 chữ số, bấm Lưu.'], L('12345678901234', '9999999999999'),
     ['Lần 1: báo đỏ dưới ô "Giá trị vượt quá giới hạn cho phép", không lưu, số đã gõ giữ nguyên', 'Lần 2: lưu được, ô hiện 9,999,999,999,999']),
    ('Ô 0 / ô trống', 'P2', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, gõ 0 vào Khách hãng Hàng hóa SL khách, các ô khác để trống.'], '0',
     ['Ở dòng phòng, ô 0 / trống hiển thị trống (placeholder "Nhập SL" / "Nhập doanh số")', 'Dòng Tỉnh/TP và dòng TỔNG hiện 0 ở cột không có số']),
    ('Phòng đã chia bộ phận thì số của phòng = tổng bộ phận', 'P1', PRE_NEW + '\nPHÒNG KINH DOANH 1 có 2 bộ phận Nhóm KD1-1, Nhóm KD1-2.',
     TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, bấm "+ Chia Bộ Phận", chọn Nhóm KD1-1, nhập Khách hãng Hàng hóa 2 / 400,000,000.', 'Bấm "+ Thêm Bộ Phận", chọn Nhóm KD1-2, nhập 3 / 600,000,000.'], '',
     ['Dòng PHÒNG KINH DOANH 1 chỉ đọc, Khách hãng Hàng hóa = 5 / 1,000,000,000', 'Dòng Hà Nội cộng đúng 5 / 1,000,000,000']),
])

G5 = ('THỐNG KÊ DÒNG TỈNH/TP & KHỐI THỐNG KÊ TOÀN PHIẾU', 'Thống kê dòng Tỉnh/TP & toàn phiếu', [
    ('Chỉ số trên dòng Tỉnh/TP', 'P0', PRE_NEW, TAO_HN + ['Quan sát dòng Thành phố Hà Nội trước khi chọn phòng.'], '',
     ['Sau tên tỉnh có 3 nhãn: "3 KVKD", "2 phòng được chia", "Đã phân 0/2 phòng"',
      'Nhãn "Đã phân 0/2 phòng" màu cam (chưa giao đủ)']),
    ('Giao đủ phòng thì nhãn chuyển xanh', 'P0', PRE_NEW,
     TAO_HN + ['Hà Nội dòng 1 chọn PHÒNG KINH DOANH 1.', 'Bấm "+ Thêm Phòng Ban", chọn PHÒNG KINH DOANH 2.', 'Xoá dòng PHÒNG KINH DOANH 2.'], '',
     ['Bước 1: "Đã phân 1/2 phòng" màu cam, còn link "+ Thêm Phòng Ban"',
      'Bước 2: "Đã phân 2/2 phòng" màu xanh, KHÔNG còn link "+ Thêm Phòng Ban"',
      'Bước 3: về "Đã phân 1/2 phòng" màu cam, link "+ Thêm Phòng Ban" hiện lại']),
    ('Bấm nhãn KVKD xem danh sách khu vực kinh doanh', 'P0', PRE_NEW + '\nKV HN 1 có 12 phường/xã, đang chia cho PHÒNG KINH DOANH 1.',
     TAO_HN + ['Bấm nhãn "3 KVKD" ở dòng Hà Nội.', 'Gõ "hn 1" (không dấu) vào ô tìm.', 'Bấm tiêu đề cột Số phường/xã.', 'Bấm Đóng.'], '',
     ['Popup "Danh sách khu vực kinh doanh", dòng phụ "Kinh doanh · Thành phố Hà Nội · 3 khu vực"',
      'Cột: Khu vực kinh doanh, Số phường/xã, Phòng ban / bộ phận đang được chia; 3 dòng; KV HN 1: 12, PHÒNG KINH DOANH 1',
      'Tìm không dấu ra đúng KV HN 1, góc phải hiện "1 / 3 dòng"; sắp xếp số phường/xã theo giá trị số',
      'Đóng popup thì bảng nhập liệu giữ nguyên']),
    ('Bấm nhãn phòng được chia xem danh sách phòng', 'P0', PRE_NEW,
     TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1.', 'Bấm nhãn "2 phòng được chia".'], '',
     ['Popup "Danh sách phòng ban được chia thị trường", dòng phụ "Kinh doanh · Thành phố Hà Nội · 2 phòng"',
      'Cột: Phòng ban, Phạm vi được chia, Phiếu phân chia thị trường, Giao chỉ tiêu trên phiếu này',
      'PHÒNG KINH DOANH 1: "Cả phòng", số phiếu phân chia, "Đã giao" màu xanh',
      'PHÒNG KINH DOANH 2: "Bộ phận: Nhóm KD2-1", "Chưa giao" màu cam']),
    ('Khối thống kê toàn phiếu', 'P0', PRE_NEW,
     TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1 nhập Khách hãng Hàng hóa 5 / 1,500,000,000 và Khách khác Dịch vụ 1 / 200,000,000.',
               'Hải Phòng chọn PHÒNG KINH DOANH 1 nhập Khách hãng Dịch vụ 2 / 300,000,000.'], '',
     ['Trên thanh tab có khối thống kê 3 ô:',
      '"Phòng ban được chia thị trường": Tổng 3 · Đã được phân 2 · Chưa được phân 1 (màu cam)',
      '"Tổng SL khách hàng đã giao": 8, Hàng hóa 5 · Dịch vụ 3',
      '"Tổng Doanh số đã giao (VNĐ)": 2,000,000,000, Hàng hóa 1,500,000,000 · Dịch vụ 500,000,000',
      'Số tự cập nhật ngay khi gõ / chọn phòng, không cần lưu']),
    ('Cách đếm phòng ở khối thống kê', 'P1', PRE_NEW, TAO_HN + ['Rê chuột vào ⓘ của ô "Phòng ban được chia thị trường".', 'Chọn đủ 2 phòng ở Hà Nội và PHÒNG KINH DOANH 1 ở Hải Phòng.'], '',
     ['Tooltip: đếm theo từng Tỉnh/TP — 1 phòng được chia ở 3 tỉnh tính 3; Chưa được phân = Tổng − Đã được phân',
      'Sau bước 2: Tổng 3 · Đã được phân 3 · Chưa được phân 0 (màu xanh)']),
    ('Thống kê cộng mọi khối kinh doanh', 'P1', PRE_NEW + '\nKhối Nghiệp vụ: Hà Nội chia cho PHÒNG DỰ ÁN 1.',
     TAO + ['Chọn Năm 2027, Khối kinh doanh = Kinh doanh, Nghiệp vụ; mỗi khối chọn khu vực Đồng bằng sông Hồng.',
            'Tab Kinh doanh: Hà Nội PHÒNG KINH DOANH 1 nhập 5 / 1,500,000,000.', 'Tab Nghiệp vụ: Hà Nội PHÒNG DỰ ÁN 1 nhập 1 / 100,000,000.'], '',
     ['Khối thống kê: Tổng 4 phòng được chia (3 của Kinh doanh + 1 của Nghiệp vụ), Đã được phân 2',
      'Tổng SL khách 6, Tổng Doanh số 1,600,000,000 (cộng cả 2 khối)']),
    ('Màn Chi tiết hiện thống kê', 'P0', PRE_EDIT, XEM + ['Bấm nhãn "3 KVKD" và "2 phòng được chia" ở dòng Hà Nội.'], '',
     ['Màn Chi tiết có khối thống kê toàn phiếu và các nhãn KVKD / phòng được chia / Đã phân X/Y phòng ở dòng Tỉnh/TP như màn Sửa',
      'Bấm nhãn mở đúng popup danh sách khu vực / danh sách phòng như ở màn Tạo / Sửa',
      'Chữ trong khối thống kê: nhãn nhỏ, số to đậm, cùng cỡ với khối thống kê ở các màn báo cáo']),
])

G6 = ('LƯU / GỬI DUYỆT', 'Lưu / Gửi duyệt', [
    ('Lưu phiếu hợp lệ', 'P0', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, nhập Khách hãng Hàng hóa 5 / 1,500,000,000.', 'Bấm Lưu.'], '',
     ['Báo lưu thành công, về danh sách', 'Phiếu mới ở đầu danh sách, Năm 2027, trạng thái Đang tạo, Người tạo = A']),
    ('Lưu không bắt cặp SL khách / Doanh số', 'P1', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, chỉ nhập SL khách 5 (bỏ trống Doanh số).', 'Bấm Lưu.'], '',
     ['Lưu được, trạng thái Đang tạo']),
    ('Lưu và gửi: có Doanh số mà thiếu SL khách', 'P0', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, chỉ nhập Doanh số 1,500,000,000.', 'Bấm Lưu và gửi.'], '',
     ['Báo đỏ dưới ô SL khách: "Bắt buộc nhập SL Khách vì đã có doanh số"', 'Phiếu không được gửi duyệt']),
    ('Lưu và gửi: có SL khách mà thiếu Doanh số', 'P0', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, chỉ nhập SL khách 5.', 'Bấm Lưu và gửi.'], '',
     ['Báo đỏ dưới ô Doanh số: "Bắt buộc nhập doanh số vì đã có SL Khách"']),
    ('Lưu và gửi phiếu không có doanh số', 'P1', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, không nhập số nào.', 'Bấm Lưu và gửi.'], '',
     ['Báo "Phiếu chưa có chỉ tiêu doanh số — không gửi được", phiếu không được gửi']),
    ('Lưu và gửi thành công', 'P0', PRE_NEW, TAO_HN + ['Hà Nội chọn PHÒNG KINH DOANH 1, nhập Khách hãng Hàng hóa 5 / 1,500,000,000.', 'Bấm Lưu và gửi.'], '',
     ['Phiếu được lưu và chuyển Chờ duyệt', 'Phiếu hiện ở lối vào "Giao chỉ tiêu chờ duyệt" của người có quyền Duyệt']),
])

G7 = ('CHI TIẾT / SỬA', 'Chi tiết / Sửa', [
    ('Giao diện màn Chi tiết', 'P0', ACC_A + '\n' + COV + '\n' + DRAFT.replace('Đang tạo', 'Đang tạo (đã bị D Từ chối 1 lần với lý do "Sai số liệu")'),
     XEM, '',
     ['Ô Khối kinh doanh và Khu vực hiện dạng chữ, có KHUNG viền nền xám như ô bị khoá (cùng kiểu ô Năm)',
      'Khối "Thông tin phiếu" KHÔNG còn nhãn trạng thái (trạng thái chỉ nằm ở tiêu đề màn)',
      'KHÔNG còn dòng "Lý do từ chối" trên màn; lý do xem ở Lịch sử thay đổi',
      'Bảng không có ô nhập, không có thùng rác, không có link Thêm / Chia']),
    ('Sửa số liệu và lưu', 'P0', PRE_EDIT, SUA + ['Đổi Doanh số Khách hãng Hàng hóa của PHÒNG KINH DOANH 1 từ 1,500,000,000 thành 1,800,000,000.', 'Bấm Lưu.'], '',
     ['Báo lưu thành công, về danh sách; mở lại Chi tiết thấy 1,800,000,000', 'Trạng thái vẫn Đang tạo']),
    ('Phiếu cũ có danh sách khách hàng vẫn xem / sửa được', 'P1',
     ACC_A + '\nPhiếu TPE_CTKD_2025.00004 lập trên hệ thống cũ (Đã duyệt) có nhập chi tiết khách hàng: 2 khách hãng Hàng hóa, doanh số 1,100,000,000.',
     [MENU, 'Bấm số phiếu TPE_CTKD_2025.00004.'], '',
     ['Hiện đủ khối, tỉnh, phòng và số như hệ thống cũ (Khách hãng Hàng hóa 2 / 1,100,000,000)', 'Không có nút / cửa sổ "Thêm / Xem Khách Hàng"']),
])

G8 = ('DUYỆT / TỪ CHỐI / HỦY DUYỆT / HỦY PHIẾU', 'Duyệt / Từ chối / Hủy duyệt / Hủy phiếu', [
    ('Từ chối ngay ở danh sách', 'P0', ACC_D + '\n' + COV + '\n' + PENDING, [MENU_CD, 'Ở dòng phiếu P1 mở menu ⋮.', 'Bấm Từ chối, nhập lý do "Sai số liệu", bấm Từ chối.'], 'Lý do: Sai số liệu',
     ['Menu ⋮ của phiếu Chờ duyệt có nút "Từ chối" (trước đây chỉ có ở màn Chi tiết)',
      'Hộp "Từ chối phiếu" có ô Lý do bắt buộc, 2 nút Hủy / Từ chối',
      'Từ chối xong phiếu về Đang tạo']),
    ('Từ chối bỏ trống lý do', 'P1', ACC_D + '\n' + PENDING, [MENU_CD, 'Ở phiếu P1 bấm ⋮ > Từ chối, để trống Lý do, bấm Từ chối.'], '',
     ['Báo đỏ dưới ô Lý do "Bắt buộc phải nhập" và thông báo "Bạn chưa nhập đầy đủ thông tin"', 'Hộp không đóng, phiếu vẫn Chờ duyệt']),
    ('Hủy duyệt bắt buộc nhập lý do', 'P0', ACC_D + '\n' + APPROVED, [MENU, 'Ở phiếu P1 bấm ⋮ > Hủy duyệt.', 'Để trống Lý do, bấm Hủy duyệt.', 'Nhập lý do "Điều chỉnh chỉ tiêu", bấm Hủy duyệt.'], 'Lý do: Điều chỉnh chỉ tiêu',
     ['Hộp "Hủy duyệt phiếu" có ô Lý do bắt buộc, 2 nút Đóng / Hủy duyệt',
      'Bước 2: báo "Bắt buộc phải nhập", không hủy duyệt',
      'Bước 3: phiếu về Đang tạo; người lập nhận thông báo kèm lý do']),
    ('Hủy phiếu bắt buộc nhập lý do', 'P0', PRE_EDIT, [MENU, 'Ở phiếu P1 bấm ⋮ > Hủy phiếu.', 'Để trống Lý do, bấm Hủy phiếu.', 'Nhập lý do "Lập nhầm", bấm Hủy phiếu.'], 'Lý do: Lập nhầm',
     ['Hộp "Hủy phiếu" có ô Lý do bắt buộc, 2 nút Đóng / Hủy phiếu',
      'Bước 2: báo "Bắt buộc phải nhập", phiếu không bị hủy',
      'Bước 3: phiếu chuyển Hủy; năm 2027 xuất hiện lại trong ô Năm khi tạo phiếu mới']),
    ('Lý do quá dài', 'P2', ACC_D + '\n' + APPROVED, [MENU, 'Ở phiếu P1 bấm ⋮ > Hủy duyệt, nhập lý do 256 ký tự, bấm Hủy duyệt.'], 'Lý do 256 ký tự',
     ['Báo "Vui lòng nhập tối đa 255 ký tự.", không hủy duyệt (Từ chối cho tối đa 1000 ký tự)']),
    ('Hủy duyệt bị chặn khi đã có phiếu theo nhân viên', 'P1', ACC_D + '\n' + APPROVED + '\nCó phiếu giao chỉ tiêu theo nhân viên TPE_CTKDNV_2027.000MM (Chờ duyệt) dùng chỉ tiêu của PHÒNG KINH DOANH 1.',
     [MENU, 'Ở phiếu P1 bấm ⋮ > Hủy duyệt, nhập lý do, bấm Hủy duyệt.'], '',
     ['Báo "Đã có phiếu giao chỉ tiêu theo nhân viên TPE_CTKDNV_2027.000MM dùng chỉ tiêu của phiếu này, cần hủy duyệt/từ chối phiếu đó trước"', 'Phiếu vẫn Đã duyệt']),
])

G9 = ('LỊCH SỬ / IN / XUẤT EXCEL', 'Lịch sử / In / Xuất Excel', [
    ('Lịch sử ghi rõ lý do từng thao tác', 'P0', ACC_D + '\nPhiếu P1 đã lần lượt: Gửi duyệt, Từ chối (lý do "Sai số liệu"), Gửi duyệt, Duyệt, Hủy duyệt (lý do "Điều chỉnh"), Hủy phiếu (lý do "Lập nhầm").',
     [MENU, 'Ở phiếu P1 bấm ⋮ > Lịch sử.'], '',
     ['Mỗi lần chuyển trạng thái là 1 dòng tiêu đề "Thay đổi trạng thái" màu cam, kèm dòng Trạng thái ghi trạng thái cũ và trạng thái mới',
      'Dòng Từ chối ghi "Lý do từ chối: Sai số liệu"; dòng Hủy duyệt ghi "Lý do hủy duyệt: Điều chỉnh"; dòng Hủy ghi "Lý do hủy: Lập nhầm"']),
    ('Lưu mà không sửa gì thì không ghi lịch sử', 'P0', PRE_EDIT, SUA + ['Không đổi gì, bấm Lưu.', 'Mở ⋮ > Lịch sử của P1.'], '',
     ['Không phát sinh dòng lịch sử Sửa mới; KHÔNG còn dòng ghi đổi Số phiếu và Năm']),
    ('Lịch sử Sửa chỉ ghi phần đổi', 'P0', PRE_EDIT, SUA + ['Đổi Doanh số Khách hãng Hàng hóa PHÒNG KINH DOANH 1 từ 1,500,000,000 thành 1,800,000,000, bấm Lưu.', 'Mở ⋮ > Lịch sử.'], '',
     ['Có 1 dòng Sửa, mục "Danh sách chỉ tiêu", dòng "Kinh doanh · Thành phố Hà Nội · PHÒNG KINH DOANH 1": "Khách hãng - Hàng hóa - Doanh số" giá trị cũ 1,500,000,000, giá trị mới 1,800,000,000',
      'Không có dòng Số phiếu / Năm']),
    ('In phiếu', 'P1', PRE_EDIT, [MENU, 'Ở phiếu P1 bấm ⋮ > In.'], '',
     ['Bản xem trước có bảng theo khối, cột SL / Doanh số theo Tỉnh/TP, phòng, bộ phận; không có danh sách khách hàng chi tiết', 'Số có dấu phẩy ngăn nghìn, khớp màn Chi tiết']),
    ('Xuất Excel 1 phiếu', 'P1', PRE_EDIT, [MENU, 'Ở phiếu P1 bấm ⋮ > Xuất Excel.'], '',
     ['Tải về file Excel; sheet khối Kinh doanh: PHÒNG KINH DOANH 1 SL khách 5, Doanh số 1,500,000,000 (ô số, có dấu ngăn nghìn)', 'Không có sheet / cột danh sách khách hàng']),
])

G10 = ('PHÂN QUYỀN', 'Phân quyền', [
    ('Chỉ người lập có quyền Tạo mới sửa được phiếu', 'P0', ACC_A + '\nTài khoản A2 cũng có quyền ' + Q_CREATE + '.\n' + DRAFT, ['Đăng nhập A2.', MENU], '',
     ['A2 không thấy nút Sửa, Gửi duyệt, Hủy phiếu ở phiếu P1 của A']),
    ('Từ chối / Hủy duyệt chỉ hiện với người có quyền Duyệt', 'P0', ACC_A + '\n' + PENDING, ['Đăng nhập A (chỉ có quyền Tạo).', MENU, 'Mở ⋮ của phiếu P1.'], '',
     ['Không có nút Duyệt, Từ chối; phiếu Đã duyệt không có nút Hủy duyệt']),
    ('Không có quyền Xem thì chỉ thấy phiếu của mình', 'P1', 'Tài khoản N không có quyền ' + Q_VIEW + ', đã lập 1 phiếu; công ty có 5 phiếu.', ['Đăng nhập N.', MENU], '',
     ['Danh sách chỉ có phiếu N lập (và phiếu N đã duyệt nếu có)']),
])

GROUPS = [G1, G2, G3, G4, G5, G6, G7, G8, G9, G10]
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']

DESC = [
    ('1. Mục đích',
     'Công ty giao chỉ tiêu kinh doanh năm (SL khách và Doanh số, tách Khách hãng / Khách khác, Hàng hóa / Dịch vụ) cho từng phòng ban '
     '(tuỳ chọn tới bộ phận) theo Khối kinh doanh > Khu vực > Tỉnh/TP. Task #11643: BỎ phần chọn chi tiết khách hàng, nhập thẳng SL '
     'và Doanh số; bản sửa lại 21-26/11 bổ sung lọc phòng theo thị trường đã chia, chỉ số dòng Tỉnh/TP và khối thống kê toàn phiếu.'),
    ('2. Đường dẫn',
     'Phân hệ Bán hàng > Kế hoạch > Giao chỉ tiêu kinh doanh > Theo phòng ban (Danh sách, Tạo, Sửa, Chi tiết).\n'
     'Lối vào thứ 2: Bán hàng > Phê Duyệt > Kế hoạch & chỉ tiêu > Giao chỉ tiêu chờ duyệt (chỉ phiếu Chờ duyệt).'),
    ('3. Phạm vi dữ liệu',
     'Ô Phòng ban ở mỗi Tỉnh/TP chỉ có phòng được chia thị trường tại tỉnh đó (Phiếu phân chia thị trường theo phòng ban ĐÃ DUYỆT của '
     'công ty, phòng thuộc khối, đang hoạt động); phòng chỉ được chia theo bộ phận thì chỉ chọn được các bộ phận đó.\n'
     'Ô Năm bỏ các năm công ty đã có phiếu còn hiệu lực (Đang tạo / Chờ duyệt / Đã duyệt); phiếu Hủy không chiếm năm.'),
    ('4. Danh sách',
     'Bấm số phiếu mở Chi tiết (không còn nút Xem). Menu ⋮: Gửi duyệt, Duyệt, Từ chối, Hủy duyệt, Hủy phiếu, In, Xuất Excel, Lịch sử '
     '— nút hiện theo trạng thái + quyền.'),
    ('5. Chức năng chính',
     'Tạo (Lưu, Lưu và gửi), Sửa, Gửi duyệt, Duyệt, Từ chối, Hủy duyệt, Hủy phiếu.\n'
     'Mỗi dòng phòng / bộ phận có 8 ô nhập: Khách hãng và Khách khác × Hàng hóa và Dịch vụ × SL khách và Doanh số (VNĐ); Tổng cộng tự tính.'),
    ('6. Quy tắc nghiệp vụ',
     'SL khách: số nguyên ≥ 0; Doanh số: ≥ 0, tối đa 2 chữ số thập phân; tối đa 13 chữ số. Lưu không bắt cặp; Gửi duyệt bắt cặp '
     'SL khách với Doanh số và phải có ít nhất 1 doanh số.\n'
     'Dòng Tỉnh/TP: "<n> KVKD", "<n> phòng được chia", "Đã phân X/Y phòng" (xanh khi X = Y, cam khi chưa đủ); giao đủ thì ẩn "+ Thêm Phòng Ban".\n'
     'Khối thống kê toàn phiếu: Phòng ban được chia (Tổng / Đã được phân / Chưa được phân, đếm theo từng Tỉnh/TP), Tổng SL khách, Tổng Doanh số (tách Hàng hóa / Dịch vụ).'),
    ('7. Luồng trạng thái',
     'Đang tạo > (Gửi duyệt) Chờ duyệt > (Duyệt) Đã duyệt. Chờ duyệt: Từ chối (bắt buộc lý do) về Đang tạo. Đã duyệt: Hủy duyệt '
     '(bắt buộc lý do) về Đang tạo. Đang tạo / Chờ duyệt: Hủy phiếu (bắt buộc lý do) chuyển Hủy. Chỉ phiếu Đang tạo sửa được.'),
    ('8. Phân quyền',
     Q_CREATE + ': tạo; sửa, gửi duyệt, hủy phiếu của mình. ' + Q_APPROVE + ': duyệt, từ chối, hủy duyệt (phiếu công ty đang làm việc).\n'
     + Q_VIEW + ' mức Tổng công ty / Công ty; không có quyền Xem thì chỉ thấy phiếu mình lập / mình duyệt.'),
    ('9. Ảnh hưởng dữ liệu',
     'Phiếu Đã duyệt là nguồn chỉ tiêu của Phiếu giao chỉ tiêu theo nhân viên và dòng "Năm trước" của phiếu năm sau; đang có phiếu theo '
     'nhân viên Chờ duyệt / Đã duyệt thì không Hủy duyệt được. Hủy duyệt phiếu phân chia thị trường làm phòng đó không còn chọn được.'),
    ('10. Chức năng bổ trợ',
     'In phiếu; Xuất Excel danh sách và từng phiếu; Lịch sử thay đổi (chuyển trạng thái ghi "Thay đổi trạng thái" + lý do; Sửa chỉ ghi '
     'phần thực sự đổi); popup danh sách khu vực kinh doanh / phòng được chia; ⓘ giải thích tiêu đề cột.'),
]

# ───────────────────────── dựng file ─────────────────────────
TNR = 'Times New Roman'
WIDTHS = {'A': 20.1, 'B': 14, 'C': 9.5, 'D': 24, 'E': 9.1, 'F': 32.1, 'G': 31.6, 'H': 22, 'I': 46.9, 'J': 30,
          'K': 12.4, 'L': 12.4, 'M': 30, 'N': 12.4, 'O': 12.4, 'P': 12.4, 'Q': 17.5, 'R': 20}
HEAD = ['Module', 'Nhóm chức năng', 'TC ID', 'Chức năng', 'Priority', 'Tiền điều kiện', 'Bước thực hiện', 'Test Data',
        'Expected Result (chi tiết)', 'Actual Result', 'Status check lần 1', 'Status check lần2', 'Ghi chú',
        'TPE TEST 1', 'TPE TEST2', 'TPE TEST 3', 'Kết quả hiện tại', 'Ghi chú TPE']


def fill(rgb):
    return PatternFill('solid', fgColor=rgb)


def build():
    wb = Workbook()
    ws = wb.active
    ws.title = 'Trang tính1'
    for k, v in WIDTHS.items():
        ws.column_dimensions[k].width = v
    wrap = Alignment(wrap_text=True, vertical='center')
    wrapc = Alignment(wrap_text=True, vertical='center', horizontal='center')

    ws['A1'] = 'MÔ TẢ CHỨC NĂNG'
    ws['A1'].font = Font(name=TNR, size=12, bold=True)
    ws['A1'].alignment = wrap
    ws.merge_cells('A1:I1')
    for i, (k, v) in enumerate(DESC):
        r = 2 + i
        ws.cell(r, 1, k).font = Font(name=TNR, size=12, bold=True)
        ws.cell(r, 1).alignment = wrap
        ws.cell(r, 2, v).font = Font(name=TNR, size=12)
        ws.cell(r, 2).alignment = wrap
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=10)
        ws.row_dimensions[r].height = 18 * max(1, v.count('\n') + 1 + len(v) // 190)

    # summary 12..17
    ws['A12'] = TITLE
    ws['A12'].font = Font(name=TNR, size=15, bold=True, color='4A86E8')
    ws['A12'].alignment = wrapc
    ws.merge_cells('A12:E16')
    ws['F12'] = 'TEST SUMMARY'
    ws['F12'].font = Font(name=TNR, size=11, bold=True, color='FFFFFF')
    ws['F12'].fill = fill('4472C4')
    ws['F12'].alignment = wrapc
    ws.merge_cells('F12:H17')
    for r in range(12, 18):
        for c in 'FGH':
            ws[f'{c}{r}'].fill = fill('4472C4')
    LAST = 300
    dns = [
        ('Số trường hợp DNS kiểm thử đạt (P):', f'=COUNTIFS(L20:L{LAST},"Passed")+COUNTIFS(K20:K{LAST},"Passed",L20:L{LAST},"")'),
        ('Số trường hợp DNS kiểm thử không đạt (F)', f'=COUNTIFS(L20:L{LAST},"Failed")+COUNTIFS(K20:K{LAST},"Failed",L20:L{LAST},"")'),
        ('Số trường hợp DNS kiểm thử đang xem xét (PE)', f'=COUNTIFS(L20:L{LAST},"Pending")+COUNTIFS(K20:K{LAST},"Pending",L20:L{LAST},"")'),
        ('Số trường hợp DNS kiểm thử chưa thực hiện', '=K17-K16'),
        ('Tổng số trường hợp DNS kiểm thử', '=SUM(K12:L14)'),
        ('Tổng số testcase', f'=COUNTIF(C20:C{LAST},"TC_*")'),
    ]
    tp = [
        ('Số trường hợp TP kiểm thử đạt (P):', f'=COUNTIF(Q20:Q{LAST},"P")'),
        ('Số trường hợp TP kiểm thử không đạt (F)', f'=COUNTIF(Q20:Q{LAST},"F")'),
        ('Số trường hợp TP kiểm thử đang xem xét (PE)', f'=COUNTIF(Q20:Q{LAST},"PE")'),
        ('Số trường hợp TP kiểm thử chưa thực hiện', '=K17-P16'),
        ('Tổng số trường hợp TP đã kiểm thử', '=SUM(P12:Q14)'),
    ]
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

    for c, h in enumerate(HEAD, 1):
        cell = ws.cell(19, c, h)
        cell.font = Font(name=TNR, size=12, bold=True)
        cell.fill = fill('FF9900')
        cell.alignment = wrapc
    ws.row_dimensions[19].height = 34

    r = 20
    n = 0
    ids = set()
    for gi, (gname, bname, tcs) in enumerate(GROUPS):
        ws.cell(r, 3, '%s. %s' % (ROMAN[gi], gname))
        for c in range(1, 19):
            ws.cell(r, c).fill = fill('D6E4F0')
            ws.cell(r, c).font = Font(name=TNR, size=12, bold=True, color='1F4E79')
            ws.cell(r, c).alignment = Alignment(vertical='center')
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=13)
        ws.row_dimensions[r].height = 24
        r += 1
        first = r
        for (fn, pr, pre, st, data, ex) in tcs:
            n += 1
            tid = 'TC_%03d' % n
            assert tid not in ids
            ids.add(tid)
            vals = {1: MODULE if r == first else None, 2: bname if r == first else None, 3: tid, 4: fn, 5: pr, 6: pre,
                    7: steps(st), 8: data or None, 9: exp(ex)}
            for c in range(1, 19):
                cell = ws.cell(r, c, vals.get(c))
                cell.font = Font(name=TNR, size=12)
                cell.alignment = wrapc if c in (3, 5, 11, 12, 17) else wrap
            ws.cell(r, 17, f'=IF(P{r}<>"",P{r},IF(O{r}<>"",O{r},IF(N{r}<>"",N{r},"")))')
            lines = max(len(pre) // 30 + pre.count('\n'), sum(1 + len(x) // 40 for x in ex), len(st) * 2)
            ws.row_dimensions[r].height = max(34, min(400, 16 * lines))
            r += 1
        ws.merge_cells(start_row=first, start_column=1, end_row=r - 1, end_column=1)
        ws.merge_cells(start_row=first, start_column=2, end_row=r - 1, end_column=2)
    last = r - 1
    dv1 = DataValidation(type='list', formula1='"Passed,Failed,Pending,Not Executed"', allow_blank=True)
    dv2 = DataValidation(type='list', formula1='"P,F,PE"', allow_blank=True)
    ws.add_data_validation(dv1)
    ws.add_data_validation(dv2)
    dv1.add(f'K21:L{last}')
    dv2.add(f'N21:P{last}')
    wb.save(OUT)
    return n, last


def check():
    banned = [r'`[a-z_]{3,}`', r'\bBE\b', r'\bFE\b', r'\bHTTP\b', r'\b(400|403|404|422)\b', r'/api/', r'localStorage',
              r'permission id', r'[\U0001F300-\U0001FAFF←-⇿✀-➿]']
    text = '\n'.join(v for _, v in DESC)
    for _, _, tcs in GROUPS:
        for tc in tcs:
            text += '\n' + '\n'.join([tc[0], tc[2], '\n'.join(tc[3]), tc[4], '\n'.join(tc[5])])
    found = {p: re.findall(p, text)[:3] for p in banned if re.findall(p, text)}
    print('!!! CON THUAT NGU / ICON:', found) if found else print('OK - sach')


if __name__ == '__main__':
    check()
    n, last = build()
    tcs = [tc for _, _, g in GROUPS for tc in g]
    p0 = sum(1 for tc in tcs if tc[1] == 'P0')
    print('TC: %d, P0: %d (%.0f%%), dòng cuối %d' % (n, p0, 100.0 * p0 / n, last))
    for i, (g, _, t) in enumerate(GROUPS):
        print('  %s. %s: %d' % (ROMAN[i], g, len(t)))
    print(OUT)
