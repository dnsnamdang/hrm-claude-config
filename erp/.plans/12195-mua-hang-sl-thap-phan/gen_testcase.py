# -*- coding: utf-8 -*-
"""Testcase Redmine #12195 — [Mua hàng] SL đặt / SL duyệt nhận số thập phân 2 chữ số (kể cả < 1).

Skill testcase-documenter, KHUÔN CHUẨN 03/11/2026 (tc_chuan.build_chuan, loai='phieu').
Chạy: python gen_testcase.py -> "testcase - SL thap phan mua hang.xlsx" (tự chạy check_tc, phải "DAT", 0 lỗi).

NGOẠI LỆ "mỗi màn 1 file": task sửa MỘT loại trường (SL đặt / SL duyệt) trên ~20 màn có sẵn ⇒ 1 file cho cả task.
Engine chỉ cho ghi cột Module ở case ĐẦU mỗi nhóm (check_tc) ⇒ tên màn ghi ở đầu cột Chức năng dạng "[PO nhập khẩu] …".

Nguồn hành vi (đọc 18/11/2026): repo TanPhatDev commit d86dd651aa (nhánh task_12195, 85 file):
- Ô nhập: type number step 0.01 min 0 + setter làm tròn 2 số (roundNumber(value, 2) || 0) — trống / không hợp lệ => 0.
- Setter có trần (tự kéo về trần, KHÔNG báo lỗi — hành vi cũ giữ nguyên): SL duyệt <= SL yêu cầu (YC gốc), SL về <= SL đặt (PI),
  SL lập HĐ <= SL PI còn lại, SL Invoice <= SL HĐ - đã Invoice - phụ lục giảm, SL giảm <= SL hợp đồng / còn lại, SL báo về <= SL hợp đồng,
  SL HĐ mua ngoài <= SL còn lại của YC; số âm => 0 ở các setter có "if (value < 0)".
- Máy chủ: min:1 -> min:0.01 ở YC gốc (SL, SL đặt tồn kho), YC nhập khẩu, HĐ nhập khẩu (khi sửa), HĐ trong nước / đơn hàng
  nguyên tắc / PLBS trong nước, Invoice, báo hàng về nhập khẩu, báo hàng về theo HĐ nguyên tắc (menu cũ).
  Câu lỗi lấy từ tệp ngôn ngữ: min.numeric = "Phải lớn hơn :min." => "Phải lớn hơn 0.01."
- PO (SL đặt hãng, Đặt tồn kho bổ sung) quy tắc cũ min:0 => cho lưu 0. PLG trong nước / mua ngoài SL giảm min:0. Báo hàng về trong nước min:0.
- Hiển thị: bộ lọc hiển thị chung (làm tròn 2 số, dấu phẩy ngăn nghìn, dấu chấm thập phân, BỎ số 0 thừa: 1.50 -> 1.5, 2.00 -> 2).
  Bản in / Excel: hàm định dạng số lượng 2 số lẻ — cũng bỏ số 0 thừa. Ô nhập kiểu số KHÔNG có dấu ngăn nghìn.
- PI so "SL về" với "SL đặt" sau khi làm tròn 2 số: 0.06 + 0.57 + 0.37 = 1 (trước đây 0.9999999999999999 bị chặn sai).
  Câu chặn: "SL về và SL đặt không bằng nhau. Vui lòng kiểm tra lại!"
- Migration đổi cột SL số nguyên -> decimal(12,2) cho YC trong nước + HĐ trong nước (trước đây 1.25 lưu thành 1).
Màn trong danh sách issue mà commit KHÔNG sửa: HĐ nguyên tắc (SL cố định 1), form YC đặt hàng trong nước (ô SL vẫn bước 1),
form YC mua ngoài (đã bước 0.01 từ trước), phiếu báo hàng về mua ngoài (ô chữ cũ), báo hàng về nhập khẩu (SL chỉ hiển thị).
"""
import os
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'hrm', '.claude', 'skills', 'testcase-documenter', 'assets'))
from tc_chuan import build_chuan  # noqa: E402

OUT = os.path.join(HERE, 'testcase - SL thap phan mua hang.xlsx')

MIN_MSG = '"Phải lớn hơn 0.01."'
PI_MSG = '"SL về và SL đặt không bằng nhau. Vui lòng kiểm tra lại!"'
NOASSIGN = '"Chưa phân công người phụ trách thương hiệu, hãng sản xuất"'


def MENU(group, item):
    return 'Vào menu Mua hàng > mục "%s" > bấm "%s".' % (group, item)


DATA_NK = ('Công ty TPE; thương hiệu B1 - hãng H1 (nhập khẩu) đã phân công người mua là tài khoản M; khách hàng KH01; '
           'hàng HH01 (ĐVT Cái) và HH02 (ĐVT Bộ) thuộc hãng H1.')
DATA_TN = ('Công ty TPE; thương hiệu B2 - hãng H2 (mua trong nước) đã phân công người mua là tài khoản M; khách hàng KH01; '
           'hàng HH03 (ĐVT Cái) và HH04 (ĐVT Bộ) thuộc hãng H2; nhà cung cấp NCC2.')
DATA_MN = ('Công ty TPE; yêu cầu đặt hàng mua ngoài YCMN-1 đã duyệt: hàng HH05 (ĐVT Cái) SL 2, chưa lập hợp đồng; '
           'nhà cung cấp NCC3.')
ACC = ('Tài khoản S: nhân viên kinh doanh phòng KD1, lập yêu cầu. Tài khoản TP: trưởng phòng KD1, có quyền '
       '"Trưởng phòng duyệt yêu cầu đặt hàng". Tài khoản M: người mua được phân công hãng.')


def T(no, func, prio, pre, steps, td, exp):
    if isinstance(pre, (list, tuple)):
        pre = '\n'.join(pre)
    if isinstance(td, (list, tuple)):
        td = '\n'.join(td)
    st = '\n'.join('%d. %s' % (i + 1, s) for i, s in enumerate(steps))
    ex = '\n'.join(x if x.startswith('- ') else '- ' + x for x in exp)
    return ('%03d' % no, func, prio, pre, st, td, ex)


class Sec(list):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx

    def add(self, func, prio, pre, steps, td, exp):
        self.append(T(len(self) + 1, func, prio, pre, steps, td, exp))


# ============================================================================ DANH SÁCH MÀN
# menu: lối vào màn danh sách; new: các bước mở form lập phiếu (sau khi vào menu_new hoặc menu)
# fld: nhãn cột ô sửa; zero: block | allow | arrive | skip_row; neg: kết quả khi gõ số âm; tran: (tiền đk, dữ liệu, kết quả) khi vượt trần
SCREENS = [
    dict(k='ycg', name='YC đặt hàng gốc', pre=DATA_NK + '\n' + ACC + '\nĐăng nhập tài khoản S.',
         menu=MENU('Tiếp nhận đặt hàng', 'Phiếu yêu cầu đặt hàng'),
         new=['Bấm Thêm mới.', 'Chọn Thương hiệu B1, Hãng sản xuất H1, Gửi tới công ty TPE.',
              'Thêm hàng HH01 và HH02; mỗi hàng chọn khách hàng KH01 và Ngày cần hợp lệ.'],
         fld='SL', save='Lưu', zero='block', fail='"Tạo yêu cầu thất bại!"',
         neg='Bấm Lưu: không lưu, báo đỏ dưới ô SL ' + MIN_MSG,
         tong='Tổng SL đặt', tien=None, edit=True, other=None),
    dict(k='ycnk', name='YC đặt hàng nhập khẩu', pre=DATA_NK + '\nĐăng nhập tài khoản S.',
         menu=MENU('Nhập khẩu', 'Yêu cầu đặt hàng nhập khẩu'),
         new=['Bấm Thêm mới.', 'Chọn Thương hiệu B1; thêm hàng HH01 và HH02, mỗi hàng chọn khách hàng KH01, Ngày cần sau hôm nay, '
              'nhập Ghi chú "Test SL lẻ".'],
         fld='SL', save='Lưu', zero='block', fail=None,
         neg='Bấm Lưu: không lưu, báo đỏ dưới ô SL ' + MIN_MSG,
         tong='ô tổng SL của từng hàng', tien=None, edit=True, other=None),
    dict(k='po_nk', name='PO nhập khẩu', pre=DATA_NK + '\nYC nhập khẩu PDHNK-A đã duyệt: HH01 và HH02 cho KH01, SL duyệt mỗi hàng 2. '
         'Đăng nhập tài khoản M.',
         menu=MENU('Nhập khẩu', 'Đơn hỏi hàng - PO'),
         new=['Bấm "Luồng mua nhập khẩu cần tổng hợp" (cùng nhóm), chọn luồng của PDHNK-A và lập Đơn hỏi hàng - PO.'],
         fld='SL đặt hãng', save='Lưu', zero='allow',
         neg='Ô SL đặt hãng tự trở về 0',
         tong='Tổng SL', tien=None, edit=True,
         other='Đặt tồn kho bổ sung', extra2='Đặt tồn kho bổ sung'),
    dict(k='pi_nk', name='PI nhập khẩu', pre=DATA_NK + '\nPO-A đã duyệt của nhà cung cấp NCC1: HH01 cho KH01 SL đặt 1.25, HH02 SL đặt 2; '
         'đơn giá HH01 = 80 USD. Đăng nhập tài khoản M.',
         menu=MENU('Nhập khẩu', 'Tổng hợp PI'),
         new=['Bấm "PI theo NCC" (cùng nhóm), chọn PO-A của NCC1 và lập PI.'],
         fld='SL về', save='Lưu', zero='arrive',
         neg='Ô SL về tự trở về 0',
         tran=('Dòng HH01 có SL đặt 1.25.', 'SL về: 1.3', 'Ô SL về tự trở về 1.25 (bằng SL đặt), không vượt'),
         tong='SL đặt', tien='Thành tiền', price='80 USD', edit=True,
         other='Số lượng của hàng khuyến mãi'),
    dict(k='hd_nk', name='HĐ mua nhập khẩu', pre=DATA_NK + '\nPI-A đã duyệt của NCC1: HH01 SL PI 1.25, HH02 SL PI 2, đơn giá HH01 = 80 USD. '
         'Đăng nhập tài khoản M.',
         menu=MENU('Nhập khẩu', 'Hợp đồng mua hàng'),
         new=['Bấm "PI theo NCC" (cùng nhóm) > thẻ Chưa lập HĐ, chọn PI-A và lập hợp đồng.'],
         fld='SL lập HĐ', save='Lưu', zero='skip_row',
         neg='Ô SL lập HĐ tự trở về 0, dòng không được đưa vào hợp đồng',
         tran=('HH01 SL PI 1.25, chưa lập hợp đồng lần nào.', 'SL lập HĐ: 1.5', 'Ô SL lập HĐ tự trở về 1.25 (SL PI còn lại), không vượt'),
         tong='SL HĐ', tien='Thành tiền', price='80 USD', edit=True,
         other='SL của hàng khuyến mãi, hàng bảo hành, hàng chênh lệch'),
    dict(k='plbs_nk', name='PLBS nhập khẩu', short=True,
         pre=DATA_NK + '\nHĐ-A (HH01 SL HĐ 1.25) đã duyệt; PI bổ sung PI-B đã duyệt: HH01 SL PI 0.75, đơn giá 80 USD. Đăng nhập tài khoản M.',
         menu=MENU('Nhập khẩu', 'Phụ lục bổ sung hợp đồng mua hàng'),
         new=['Bấm Thêm mới, chọn HĐ-A và PI bổ sung PI-B.'],
         fld='SL lập HĐ', save='Lưu', zero='skip_row', neg='Ô SL lập HĐ tự trở về 0',
         tong='SL HĐ', tien='Thành tiền', price='80 USD', edit=False, other=None),
    dict(k='plg_nk', name='PLG nhập khẩu', pre=DATA_NK + '\nHĐ-A đã duyệt: HH01 (đặt cho KH01) SL hợp đồng 1.25, đơn giá 80 USD. Đăng nhập tài khoản M.',
         menu=MENU('Nhập khẩu', 'Phụ lục giảm hợp đồng mua hàng'),
         new=['Bấm Thêm mới, chọn HĐ-A.'],
         fld='SL giảm', save='Lưu', zero='allow', neg='Ô SL giảm tự trở về 0',
         tran=('HH01 SL hợp đồng 1.25.', 'SL giảm: 2', 'Ô SL giảm tự trở về 1.25 (bằng SL hợp đồng), không vượt'),
         tong=None, tien='Thành tiền', price='80 USD', edit=False, other=None),
    dict(k='inv', name='Invoice', pre=DATA_NK + '\nHĐ-A đã duyệt: HH01 SL HĐ 1.25, chưa có Invoice; đơn giá 80 USD. Có sẵn 1 tệp PDF để đính kèm. '
         'Đăng nhập tài khoản M.',
         menu=MENU('Nhập khẩu', 'Danh sách Invoice'),
         new=['Bấm Thêm mới, chọn HĐ-A, đính kèm 1 tệp PDF.'],
         fld='SL Invoice', save='Lưu', zero='block', fail='"Tạo Invoice thất bại!"',
         neg='Ô SL Invoice tự trở về 0; bấm Lưu bị chặn ' + MIN_MSG,
         tran=('HH01 SL HĐ 1.25, SL đã Invoice 0.5.', 'SL Invoice: 1', 'Ô SL Invoice tự trở về 0.75 (1.25 - 0.5), không vượt'),
         tong='Tổng SL', tien='Thành tiền', price='80 USD', edit=True,
         other='SL của hàng khuyến mãi'),
    dict(k='yc_tn', name='YC đặt hàng trong nước', pre=DATA_TN + '\nĐăng nhập tài khoản S.',
         menu=MENU('Mua trong nước theo hãng', 'Yêu cầu đặt hàng trong nước theo hãng'),
         new=['Bấm Thêm mới.', 'Chọn Thương hiệu B2; thêm HH03 và HH04, mỗi hàng chọn khách hàng KH01 và Ngày cần hợp lệ.'],
         fld='SL', save='Lưu', zero='unknown', neg='Ghi nhận kết quả thực tế (ô chưa đổi bước nhập, xem mục 9)',
         tong='SL đặt', tien=None, edit=True, other=None),
    dict(k='po_tn', name='PO trong nước', pre=DATA_TN + '\nYC trong nước PDHTN-A đã duyệt: HH03, HH04 cho KH01, SL duyệt mỗi hàng 2; '
         'NCC2 có hợp đồng nguyên tắc HĐNT-1 với đơn giá HH03 = 2,000,000 VND. Đăng nhập tài khoản M.',
         menu=MENU('Mua trong nước theo hãng', 'Đơn hỏi hàng - PO'),
         new=['Bấm "Luồng mua trong nước theo hãng" (cùng nhóm), chọn luồng của PDHTN-A và lập Đơn hỏi hàng - PO theo HĐNT-1.'],
         fld='SL đặt hãng', save='Lưu', zero='allow', neg='Ô SL đặt hãng tự trở về 0',
         tong='Tổng SL', tien='Thành tiền', price='2,000,000 VND', edit=True,
         other='Đặt tồn kho bổ sung', extra2='Đặt tồn kho bổ sung'),
    dict(k='pi_tn', name='PI trong nước', pre=DATA_TN + '\nPO-T đã duyệt của NCC2: HH03 cho KH01 SL đặt 1.25, HH04 SL đặt 2; đơn giá HH03 = '
         '2,000,000 VND. Đăng nhập tài khoản M.',
         menu=MENU('Mua trong nước theo hãng', 'Danh sách PI'),
         new=['Bấm "PI theo NCC" (cùng nhóm), chọn PO-T của NCC2 và lập PI.'],
         fld='SL về', save='Lưu', zero='arrive', neg='Ô SL về tự trở về 0',
         tran=('Dòng HH03 có SL đặt 1.25.', 'SL về: 1.3', 'Ô SL về tự trở về 1.25 (bằng SL đặt), không vượt'),
         tong='SL đặt', tien='Thành tiền', price='2,000,000 VND', edit=True, other='Số lượng của hàng khuyến mãi'),
    dict(k='hd_tn', name='HĐ mua trong nước', pre=DATA_TN + '\nPI-T đã duyệt của NCC2: HH03 SL PI 1.25, HH04 SL PI 2; đơn giá HH03 = 2,000,000 VND. '
         'Đăng nhập tài khoản M.',
         menu=MENU('Mua trong nước theo hãng', 'Hợp đồng mua hàng'),
         new=['Bấm "PI theo NCC" (cùng nhóm) > thẻ Chưa lập HĐ, chọn PI-T và lập hợp đồng.'],
         fld='SL lập HĐ', save='Lưu', zero='skip_row', neg='Ô SL lập HĐ tự trở về 0, dòng không được đưa vào hợp đồng',
         tran=('HH03 SL PI 1.25, chưa lập hợp đồng lần nào.', 'SL lập HĐ: 1.5', 'Ô SL lập HĐ tự trở về 1.25 (SL PI còn lại), không vượt'),
         tong='SL HĐ', tien='Thành tiền', price='2,000,000 VND', edit=True, other='SL của hàng khuyến mãi'),
    dict(k='dhnt', name='Đơn hàng nguyên tắc', short=True,
         pre=DATA_TN + '\nNCC2 có hợp đồng nguyên tắc HĐNT-1 đã duyệt; PI-N theo HĐNT-1 đã duyệt: HH03 SL PI 1.25, đơn giá 2,000,000 VND. '
         'Đăng nhập tài khoản M.',
         menu=MENU('Mua trong nước theo hãng', 'Đơn hàng nguyên tắc'),
         new=['Bấm Thêm mới, chọn HĐNT-1 và PI-N.'],
         fld='SL lập HĐ', save='Lưu', zero='skip_row', neg='Ô SL lập HĐ tự trở về 0',
         tong='SL HĐ', tien='Thành tiền', price='2,000,000 VND', edit=False, other=None),
    dict(k='plbs_tn', name='PLBS trong nước', short=True,
         pre=DATA_TN + '\nHĐ-T (HH03 SL HĐ 1.25) đã duyệt; PI bổ sung PI-T2 đã duyệt: HH03 SL PI 0.75, đơn giá 2,000,000 VND. Đăng nhập tài khoản M.',
         menu=MENU('Mua trong nước theo hãng', 'Phụ lục bổ sung hợp đồng mua hàng'),
         new=['Bấm Thêm mới, chọn HĐ-T và PI bổ sung PI-T2.'],
         fld='SL lập HĐ', save='Lưu', zero='skip_row', neg='Ô SL lập HĐ tự trở về 0',
         tong='SL HĐ', tien='Thành tiền', price='2,000,000 VND', edit=False, other=None),
    dict(k='bhv_tn', name='Phiếu báo hàng về trong nước', pre=DATA_TN + '\nHĐ-T đã duyệt: HH03 SL Hợp đồng 1.25, HH04 SL Hợp đồng 2, chưa báo về. '
         'Đăng nhập tài khoản M.',
         menu=MENU('Mua trong nước theo hãng', 'Phiếu báo hàng về'),
         new=['Bấm Thêm mới, chọn HĐ-T.'],
         fld='SL', save='Lưu', zero='allow', neg='Ô SL tự trở về 0',
         tran=('HH03 SL Hợp đồng 1.25.', 'SL: 1.3', 'Ô SL tự trở về 1.25 (bằng SL Hợp đồng), không vượt'),
         tong='Tổng SL', tien=None, edit=False, other=None),
    dict(k='hd_mn', name='HĐ mua hàng ngoài', pre=DATA_MN + '\nĐơn giá HH05 = 2,000,000 VND. Đăng nhập tài khoản M.',
         menu=MENU('Mua ngoài', 'Danh sách hợp đồng mua hàng ngoài'),
         new=['Bấm Thêm mới, chọn NCC3 và yêu cầu YCMN-1.'],
         fld='SL lập HĐ', save='Lưu', zero='allow', neg='Ô SL lập HĐ tự trở về 0',
         tran=('HH05 còn 2 chưa lập hợp đồng.', 'SL lập HĐ: 2.5', 'Ô SL lập HĐ tự trở về 2 (SL còn lại của yêu cầu), không vượt'),
         tong='SL', tien='Thành tiền', price='2,000,000 VND', edit=True, other='SL của hàng khuyến mãi'),
    dict(k='pl_mn', name='Phụ lục HĐ mua hàng ngoài', short=True,
         pre=DATA_MN + '\nHĐ mua ngoài HĐMN-1 đã duyệt với HH05 SL 1.25; YCMN-1 còn 0.75 chưa lập. Đơn giá 2,000,000 VND. Đăng nhập tài khoản M.',
         menu=MENU('Mua ngoài', 'Danh sách phụ lục hợp đồng mua hàng ngoài'),
         new=['Bấm Thêm mới, chọn HĐMN-1 và yêu cầu YCMN-1.'],
         fld='SL lập HĐ', save='Lưu', zero='allow', neg='Ô SL lập HĐ tự trở về 0',
         tong='SL', tien='Thành tiền', price='2,000,000 VND', edit=False, other=None),
    dict(k='plg_mn', name='PL giảm HĐ mua hàng ngoài',
         pre=DATA_MN + '\nHĐ mua ngoài HĐMN-1 đã duyệt với HH05 SL 1.25, chưa giảm lần nào. Đơn giá 2,000,000 VND. Đăng nhập tài khoản M.',
         menu=MENU('Mua ngoài', 'Danh sách phụ lục giảm hợp đồng mua hàng ngoài'),
         new=['Bấm Thêm mới, chọn HĐMN-1.'],
         fld='SL giảm', save='Lưu', zero='allow', neg='Ô SL giảm tự trở về 0',
         tran=('HH05 SL Còn lại trên HĐ 1.25.', 'SL giảm: 2', 'Ô SL giảm tự trở về 1.25 (SL Còn lại trên HĐ), không vượt'),
         tong=None, tien='Thành tiền giảm', price='2,000,000 VND', edit=False, other='SL giảm của hàng khuyến mãi'),
]
SC = {s['k']: s for s in SCREENS}


def tag(s, text):
    return '[%s] %s' % (s['name'], text)


def money(s, qty):
    """Thành tiền mẫu theo đơn giá của màn."""
    if s.get('price') == '80 USD':
        return {'1.25': '100', '0.05': '4', '0.5': '40', '12.34': '987.2'}[qty] + ' USD'
    return {'1.25': '2,500,000', '0.05': '100,000', '0.5': '1,000,000', '12.34': '24,680,000'}[qty] + ' VND'


# ============================================================================ I. THÊM MỚI
S1 = Sec(1)
for s in SCREENS:
    steps0 = [s['menu']] + s['new']
    f = s['fld']
    S1.add(tag(s, 'Nhập %s nhỏ hơn 1 lưu đúng' % f), 'P0', s['pre'],
           steps0 + ['Dòng HH thứ nhất nhập %s = 0.5, dòng thứ hai nhập %s = 0.05 (gõ từng ký tự, dấu chấm thập phân).' % (f, f),
                     'Bấm %s.' % s['save'], 'Mở lại phiếu vừa lưu.'],
           ['%s dòng 1: 0.5' % f, '%s dòng 2: 0.05' % f],
           ['Khi gõ, ô giữ đúng "0.5" và "0.05" — KHÔNG bị nhảy thành 5 hay 0',
            'Lưu thành công, quay về danh sách',
            'Mở lại: dòng 1 hiện 0.5, dòng 2 hiện 0.05'])
    if s.get('short'):
        S1.add(tag(s, 'Nhập 1.25 và số 3 chữ số lẻ lưu đúng'), 'P0', s['pre'],
               steps0 + ['Nhập %s = 1.255 ở dòng đầu, rời ô.' % f, 'Bấm %s, mở lại phiếu.' % s['save']],
               '%s: 1.255' % f,
               ['Rời ô: ô tự hiện 1.25 (làm tròn còn 2 chữ số lẻ)', 'Lưu thành công; mở lại hiện 1.25'])
        if s.get('tien'):
            S1.add(tag(s, '%s = SL lẻ × đơn giá' % s['tien']), 'P0', s['pre'] + '\nĐơn giá hàng dòng đầu: %s.' % s['price'],
                   steps0 + ['Nhập %s = 1.25 ở dòng đầu.' % f, 'Quan sát cột %s của dòng.' % s['tien']],
                   ['%s: 1.25' % f, 'Đơn giá: %s' % s['price']],
                   ['Cột %s = %s (1.25 × %s)' % (s['tien'], money(s, '1.25'), s['price']),
                    'Tổng tiền phiếu cộng đúng phần lẻ'])
        continue
    S1.add(tag(s, 'Nhập %s 1.25 và 12.34 lưu đúng' % f), 'P0', s['pre'],
           steps0 + ['Dòng 1 nhập %s = 1.25, dòng 2 nhập %s = 12.34.' % (f, f), 'Bấm %s.' % s['save'], 'Mở lại phiếu.'],
           ['%s dòng 1: 1.25' % f, '%s dòng 2: 12.34' % f],
           ['Lưu thành công', 'Mở lại: hiện đúng 1.25 và 12.34, không bị cắt thành 1 và 12'])
    S1.add(tag(s, 'Nhập 3 chữ số lẻ tự làm tròn còn 2'), 'P0', s['pre'],
           steps0 + ['Dòng 1 nhập %s = 1.255, dòng 2 nhập 1.256; rời ô.' % f, 'Bấm %s, mở lại phiếu.' % s['save']],
           ['%s dòng 1: 1.255' % f, '%s dòng 2: 1.256' % f],
           ['Rời ô: dòng 1 tự hiện 1.25, dòng 2 tự hiện 1.26 (tối đa 2 chữ số lẻ)',
            'Lưu và mở lại: 1.25 và 1.26 — không còn chữ số lẻ thứ 3'])
    z = s['zero']
    if z == 'block':
        exp = ['Không lưu, phiếu ở lại màn nhập',
               'Báo đỏ ngay dưới ô %s của 2 dòng: %s' % (f, MIN_MSG),
               'Lưu ý: để trống cũng được hiểu là 0 nên ra cùng câu báo (không phải "Bắt buộc phải nhập")']
        if s.get('fail'):
            exp.insert(1, 'Hiện thông báo %s' % s['fail'])
        S1.add(tag(s, '%s = 0 hoặc để trống bị chặn' % f), 'P0', s['pre'],
               steps0 + ['Dòng 1 nhập %s = 0, dòng 2 xoá trống ô %s.' % (f, f), 'Bấm %s.' % s['save']],
               ['%s dòng 1: 0' % f, '%s dòng 2: (trống)' % f], exp)
        S1.add(tag(s, '%s = 0.01 là mức nhỏ nhất được lưu' % f), 'P1', s['pre'],
               steps0 + ['Nhập %s = 0.01 ở dòng 1, dòng 2 nhập 1.' % f, 'Bấm %s.' % s['save']],
               ['%s dòng 1: 0.01' % f, '%s dòng 2: 1' % f],
               ['Lưu thành công (0.01 hợp lệ dù câu báo lỗi ghi "Phải lớn hơn 0.01.")', 'Mở lại hiện 0.01'])
    elif z == 'allow':
        S1.add(tag(s, '%s = 0 giữ quy tắc cũ' % f), 'P1', s['pre'],
               steps0 + ['Dòng 1 nhập %s = 0, dòng 2 nhập 1.25.' % f, 'Bấm %s.' % s['save']],
               ['%s dòng 1: 0' % f, '%s dòng 2: 1.25' % f],
               ['Ô %s không bị chặn ở mức 0 (quy tắc cũ cho phép 0 — task chỉ mở rộng số lẻ, không đổi mức sàn này)' % f,
                'Dòng 2 lưu đúng 1.25'])
    elif z == 'arrive':
        S1.add(tag(s, 'Tổng SL về khác SL đặt bị chặn'), 'P0', s['pre'],
               steps0 + ['Dòng HH01/HH03 (SL đặt 1.25) nhập SL về = 1.2.', 'Bấm %s.' % s['save']],
               'SL về: 1.2 (SL đặt 1.25)',
               ['Không lưu, hiện thông báo %s' % PI_MSG, 'Sửa SL về = 1.25 rồi Lưu: lưu thành công'])
    elif z == 'skip_row':
        S1.add(tag(s, '%s = 0 thì dòng không vào hợp đồng' % f), 'P1', s['pre'],
               steps0 + ['Dòng 1 nhập %s = 0, dòng 2 giữ 2.' % f, 'Bấm %s, mở lại hợp đồng.' % s['save']],
               ['%s dòng 1: 0' % f, '%s dòng 2: 2' % f],
               ['Hợp đồng chỉ có dòng 2 (SL 2); dòng SL 0 không được đưa vào (giữ như cũ)'])
    else:
        S1.add(tag(s, '%s = 0 hoặc để trống' % f), 'P2', s['pre'],
               steps0 + ['Dòng 1 nhập %s = 0, dòng 2 để trống.' % f, 'Bấm %s.' % s['save']],
               ['%s dòng 1: 0' % f, '%s dòng 2: (trống)' % f],
               ['Ghi nhận kết quả thực tế vào cột KQ: task không đổi quy tắc chặn của màn này (xem mục 9)'])
    S1.add(tag(s, 'Nhập số âm'), 'P1', s['pre'],
           steps0 + ['Nhập %s = -1 ở dòng 1, rời ô.' % f, 'Bấm %s.' % s['save']],
           '%s: -1' % f, [s['neg'], 'Không có dòng nào được lưu với số âm'])
    S1.add(tag(s, 'Số nguyên vẫn nhập bình thường'), 'P1', s['pre'],
           steps0 + ['Dòng 1 nhập %s = 3 (nếu có trần thì nhập bằng trần), dòng 2 nhập 1.' % f, 'Bấm %s, mở lại.' % s['save']],
           ['%s dòng 1: 3' % f, '%s dòng 2: 1' % f],
           ['Lưu thành công', 'Mở lại hiện 3 và 1 — không hiện 3.00 / 1.00'])
    if s.get('tran'):
        p, d, r = s['tran']
        S1.add(tag(s, 'Vượt trần với số lẻ vẫn bị giữ ở trần'), 'P0', s['pre'] + '\n' + p,
               steps0 + ['Nhập %s vượt trần (xem Test Data), rời ô.' % f], d,
               [r, 'Lưu ý: đây là hành vi cũ của màn (tự kéo về trần), task chỉ cho trần nhận số lẻ'])
    if s.get('tien'):
        S1.add(tag(s, '%s = SL lẻ × đơn giá' % s['tien']), 'P0', s['pre'],
               steps0 + ['Dòng 1 nhập %s = 1.25, dòng 2 nhập 0.05.' % f, 'Quan sát cột %s từng dòng và tổng tiền.' % s['tien']],
               ['%s dòng 1: 1.25; dòng 2: 0.05' % f, 'Đơn giá mỗi dòng: %s' % s['price']],
               ['Dòng 1: %s = %s' % (s['tien'], money(s, '1.25')),
                'Dòng 2: %s = %s' % (s['tien'], money(s, '0.05')),
                'Tổng tiền = cộng 2 dòng, không làm tròn SL về số nguyên trước khi nhân'])
    if s.get('tong'):
        S1.add(tag(s, 'Dòng tổng SL không hiện số lẻ dài'), 'P0', s['pre'],
               steps0 + ['Hàng HH thứ nhất: 2 khách / 2 dòng nhập %s = 0.1 và 0.2 (hoặc 2 đợt / 2 dòng tuỳ màn).' % f,
                         'Quan sát cột %s.' % s['tong']],
               ['%s: 0.1' % f, '%s: 0.2' % f],
               ['Cột %s hiện 0.3' % s['tong'], 'KHÔNG hiện 0.30000000000000004 hay 0.29999999999999998'])
    if s.get('extra2'):
        S1.add(tag(s, '%s nhận số lẻ' % s['extra2']), 'P0', s['pre'],
               steps0 + ['Ở dòng "%s" của HH thứ nhất nhập 0.75; SL đặt hãng của khách giữ 2.' % s['extra2'],
                         'Quan sát cột Tổng SL; bấm %s, mở lại.' % s['save']],
               '%s: 0.75' % s['extra2'],
               ['Tổng SL = 2.75 (cộng số, KHÔNG nối chuỗi thành 20.75 / 2.000.75)', 'Mở lại: %s hiện 0.75' % s['extra2']])
    if s.get('other'):
        S1.add(tag(s, 'Ô không thuộc phạm vi giữ nguyên hành vi'), 'P2', s['pre'],
               steps0 + ['Nhập vào ô %s giá trị 1.5.' % s['other'], 'Bấm %s.' % s['save']],
               '%s: 1.5' % s['other'],
               ['Ô %s chạy đúng như trước khi sửa (task KHÔNG đổi các ô SL khuyến mãi / bảo hành / chênh lệch / ô phụ)' % s['other'],
                'So với bản đang chạy trên môi trường thật: cùng kết quả'])

# Gõ dấu phẩy — bẫy chung, ghi cho 2 màn tiêu biểu
for k in ('ycg', 'po_nk'):
    s = SC[k]
    S1.add(tag(s, 'Gõ dấu phẩy thập phân không bị hiểu sai'), 'P1', s['pre'],
           [s['menu']] + s['new'] + ['Gõ %s = 1,25 (dấu phẩy), rời ô.' % s['fld']],
           '%s: 1,25' % s['fld'],
           ['Hệ thống KHÔNG hiểu thành 125', 'Ô số không nhận dấu phẩy: giá trị coi như 0 / trống — phải gõ dấu chấm 1.25',
            'Ghi lại hành vi thực tế của trình duyệt vào cột KQ (xem mục 9)'])
    S1.add(tag(s, 'Mũi tên tăng giảm của ô số'), 'P2', s['pre'],
           [s['menu']] + s['new'] + ['Nhập %s = 1.25, bấm mũi tên lên ở ô 1 lần.' % s['fld']],
           '%s: 1.25' % s['fld'], ['Ô thành 1.26 (bước 0.01)'])

# Tự do — mỗi màn của luồng tự do 1 case lưu số lẻ
TUDO = [('Yêu cầu đặt hàng trong nước tự do', 'YC đặt hàng trong nước tự do', 'SL'),
        ('Danh sách đơn hỏi hàng - PO', 'PO tự do', 'SL đặt hãng'),
        ('Danh sách PI', 'PI tự do', 'SL về'),
        ('Hợp đồng mua hàng', 'HĐ mua tự do', 'SL lập HĐ'),
        ('Phụ lục bổ sung hợp đồng mua hàng', 'PLBS tự do', 'SL lập HĐ'),
        ('Danh sách phiếu báo hàng về', 'Báo hàng về tự do', 'SL')]
for item, nm, f in TUDO:
    S1.add('[%s] Nhập %s 0.5 và 1.25 lưu đúng' % (nm, f), 'P0',
           DATA_TN.replace('B2 - hãng H2 (mua trong nước)', 'B3 - hãng H3 (mua trong nước tự do)') +
           '\nPhiếu trước của luồng tự do đã duyệt, còn SL đủ để lập (HH03 còn 2). Đăng nhập tài khoản M (lập YC thì tài khoản S).',
           [MENU('Mua trong nước tự do', item), 'Lập phiếu mới từ phiếu trước của luồng (như luồng theo hãng).',
            'Dòng 1 nhập %s = 0.5, dòng 2 nhập 1.25.' % f, 'Bấm Lưu, mở lại.'],
           ['%s dòng 1: 0.5' % f, '%s dòng 2: 1.25' % f],
           ['Lưu thành công', 'Mở lại hiện 0.5 và 1.25 (không cắt thành 0 và 1)'])

# ============================================================================ II. CHỈNH SỬA
S2 = Sec(2)
for s in SCREENS:
    if not s.get('edit'):
        continue
    f = s['fld']
    pre = s['pre'] + '\nĐã có phiếu %s ở trạng thái còn được sửa: dòng 1 %s = 1.25, dòng 2 %s = 0.05.' % (s['name'], f, f)
    S2.add(tag(s, 'Mở Sửa hiện đúng phần lẻ đã lưu'), 'P0', pre,
           [s['menu'], 'Mở phiếu trên, bấm Sửa.'], '—',
           ['Ô %s dòng 1 hiện 1.25, dòng 2 hiện 0.05' % f, 'Không hiện 1 / 0, không hiện 1.2500',
            'Các cột tổng và thành tiền tính lại đúng từ SL lẻ ngay khi mở'])
    S2.add(tag(s, 'Sửa SL lẻ rồi lưu lại'), 'P1', pre,
           [s['menu'], 'Mở phiếu, bấm Sửa.', 'Đổi %s dòng 1 từ 1.25 thành 0.75, dòng 2 giữ nguyên.' % f, 'Bấm Lưu, mở lại.'],
           '%s dòng 1: 0.75' % f,
           ['Lưu thành công', 'Mở lại: dòng 1 = 0.75, dòng 2 = 0.05 (không bị đổi khi không sửa)'])
    if s['zero'] == 'block':
        S2.add(tag(s, 'Sửa về 0 bị chặn'), 'P0', pre,
               [s['menu'], 'Mở phiếu, bấm Sửa.', 'Đổi %s dòng 1 thành 0.' % f, 'Bấm Lưu.'],
               '%s: 0' % f, ['Không lưu, báo đỏ dưới ô %s: %s' % (f, MIN_MSG), 'Dữ liệu cũ (1.25) giữ nguyên trên hệ thống'])
S2.add(tag(SC['hd_nk'], 'Sửa hợp đồng: SL dòng hàng = 0 bị chặn'), 'P0',
       SC['hd_nk']['pre'] + '\nHĐ-A đang ở trạng thái cho sửa (đã bị Không duyệt), HH01 SL HĐ 1.25.',
       [SC['hd_nk']['menu'], 'Mở HĐ-A, bấm Sửa.', 'Đổi SL lập HĐ của HH01 thành 0.', 'Bấm Lưu.'], 'SL lập HĐ: 0',
       ['Không lưu, báo %s tại dòng HH01 (khi sửa, mức sàn là 0.01)' % MIN_MSG])

# ============================================================================ III. DUYỆT PHIẾU
S3 = Sec(3)
ycg = SC['ycg']
PRE_D = ycg['pre'].replace('Đăng nhập tài khoản S.', '') + \
    'YC gốc PDH-A ở trạng thái Chờ TP duyệt: HH01 cho KH01 SL yêu cầu 1.25; HH02 đặt tồn kho SL yêu cầu 0.5.\nĐăng nhập tài khoản TP.'
MENU_D = ycg['menu']
S3.add(tag(ycg, 'TP duyệt với SL duyệt lẻ'), 'P0', PRE_D,
       [MENU_D, 'Mở PDH-A.', 'Ô SL duyệt của HH01 nhập 0.75; ô SL duyệt đặt tồn kho của HH02 nhập 0.05.', 'Bấm "Duyệt và gửi".',
        'Mở lại PDH-A.'],
       ['SL duyệt HH01: 0.75', 'SL duyệt đặt tồn kho HH02: 0.05'],
       ['Duyệt thành công', 'Cột SL yêu cầu: 1.25 / 0.5; cột SL duyệt: 0.75 / 0.05', 'Tổng SL đặt tính theo SL duyệt, không số rác'])
S3.add(tag(ycg, 'SL duyệt lớn hơn SL yêu cầu bị giữ ở trần'), 'P0', PRE_D,
       [MENU_D, 'Mở PDH-A.', 'Ô SL duyệt của HH01 nhập 1.3; ô SL duyệt đặt tồn kho của HH02 nhập 0.51; rời ô.'],
       ['SL duyệt HH01: 1.3 (SL yêu cầu 1.25)', 'SL duyệt tồn kho HH02: 0.51 (SL yêu cầu 0.5)'],
       ['Ô HH01 tự về 1.25, ô HH02 tự về 0.5 — không vượt SL yêu cầu',
        'Lưu ý: so sánh trên số lẻ — 1.3 > 1.25 và 0.51 > 0.5 đều bị giữ lại'])
S3.add(tag(ycg, 'SL duyệt 3 chữ số lẻ tự làm tròn'), 'P1', PRE_D,
       [MENU_D, 'Mở PDH-A.', 'Ô SL duyệt HH01 nhập 0.125, rời ô.'], 'SL duyệt: 0.125',
       ['Ô tự hiện 0.13 (làm tròn 2 chữ số lẻ)'])
S3.add(tag(ycg, 'Mặc định SL duyệt bằng SL yêu cầu lẻ'), 'P1', PRE_D, [MENU_D, 'Mở PDH-A, chưa sửa gì.'], '—',
       ['Ô SL duyệt HH01 điền sẵn 1.25, HH02 điền sẵn 0.5 (không bị làm tròn thành 1 / 1)'])
S3.add(tag(ycg, 'Kế hoạch mua hàng tiếp nhận với SL lẻ'), 'P0',
       PRE_D.replace('Chờ TP duyệt', 'đã được TP duyệt (SL duyệt HH01 0.75, HH02 0.05)').replace('Đăng nhập tài khoản TP.',
                                                                                              'Đăng nhập tài khoản M.'),
       [MENU_D, 'Mở PDH-A.', 'Giữ SL duyệt như hiện có, bấm "Kế hoạch mua hàng tiếp nhận".'], '—',
       ['Tiếp nhận thành công', 'Phiếu yêu cầu đặt hàng nhập khẩu sinh ra mang đúng SL 0.75 và 0.05'])
S3.add(tag(ycg, 'Duyệt SL duyệt = 0'), 'P2', PRE_D,
       [MENU_D, 'Mở PDH-A.', 'Ô SL duyệt HH01 nhập 0, bấm "Duyệt và gửi".'], 'SL duyệt: 0',
       ['Ghi nhận kết quả thực tế: task không đổi quy tắc SL duyệt = 0 ở bước duyệt (xem mục 9)'])

# ============================================================================ IV. KHÔNG DUYỆT PHIẾU
S4 = Sec(4)
hd = SC['hd_nk']
S4.add(tag(hd, 'Không duyệt trả lại đúng SL lẻ cho PI'), 'P0',
       hd['pre'] + '\nHĐ-A đang chờ duyệt, lập từ PI-A với HH01 SL lập HĐ 1.25. Đăng nhập người duyệt hợp đồng.',
       [hd['menu'], 'Mở HĐ-A, bấm Không duyệt, nhập lý do, xác nhận.', 'Vào "PI theo NCC" > thẻ Chưa lập HĐ, tìm PI-A.'], '—',
       ['HĐ-A về trạng thái bị Không duyệt', 'PI-A quay lại thẻ Chưa lập HĐ, HH01 còn 1.25 được lập HĐ (không còn 0.25 hay 1)'])
S4.add(tag(SC['ycg'], 'TP Không duyệt giữ nguyên SL lẻ'), 'P1', PRE_D,
       [MENU_D, 'Mở PDH-A, bấm "Không duyệt".', 'Đăng nhập S, mở PDH-A bấm Sửa.'], '—',
       ['Phiếu trả về người lập', 'Ô SL HH01 vẫn 1.25, SL đặt tồn kho HH02 vẫn 0.5'])

# ============================================================================ V. XEM CHI TIẾT
S5 = Sec(5)
VIEW = [('ycg', 'SL yêu cầu, SL duyệt, Tổng SL đặt'), ('ycnk', 'SL đặt, SL yêu cầu, SL duyệt'),
        ('po_nk', 'Tổng SL, SL duyệt, SL đặt hãng, Đặt tồn kho bổ sung'), ('pi_nk', 'SL đặt, SL về, Thành tiền'),
        ('plg_nk', 'SL hợp đồng, SL giảm'), ('inv', 'SL HĐ, SL đã Invoice, Tổng SL'),
        ('yc_tn', 'SL đặt, SL yêu cầu, SL duyệt'), ('po_tn', 'Tổng SL, Đặt tồn kho bổ sung'), ('pi_tn', 'SL đặt, SL về'),
        ('hd_tn', 'SL HĐ, Thành tiền'), ('bhv_tn', 'SL Hợp đồng, SL'), ('plg_mn', 'SL, SL giảm')]
for k, cols in VIEW:
    s = SC[k]
    S5.add(tag(s, 'Màn chi tiết hiện đủ phần lẻ'), 'P0',
           s['pre'] + '\nPhiếu đã lưu: dòng 1 = 1.25, dòng 2 = 0.05, dòng 3 = 1234.56 (nếu màn có trần thì phiếu trước đủ SL).',
           [s['menu'], 'Bấm mã phiếu để mở chi tiết.', 'Quan sát các cột %s.' % cols], '—',
           ['Dòng 1 hiện 1.25, dòng 2 hiện 0.05, dòng 3 hiện 1,234.56 (dấu phẩy ngăn nghìn, dấu chấm thập phân)',
            'Không còn cột nào hiện số nguyên bị làm tròn (1 / 0 / 1,235)',
            'Dòng tổng cộng đúng: 1,235.86'])
S5.add(tag(SC['ycg'], 'Bỏ số 0 thừa khi hiển thị'), 'P1', SC['ycg']['pre'] + '\nPDH-B đã lưu: HH01 SL 1.50, HH02 SL 2.',
       [SC['ycg']['menu'], 'Mở chi tiết PDH-B.'], '—',
       ['HH01 hiện 1.5, HH02 hiện 2 (không hiện 1.50 / 2.00) — đúng thiết kế, không phải mất phần lẻ'])
S5.add('[Báo hàng về nhập khẩu] SL lẻ lấy từ Invoice hiển thị đúng', 'P0',
       DATA_NK + '\nInvoice INV-A đã duyệt: HH01 SL 1.25 (cho KH01), HH02 SL 0.5.',
       [MENU('Nhập khẩu', 'Danh sách báo hàng về'), 'Lập phiếu báo hàng về từ INV-A, bấm Lưu.', 'Mở chi tiết phiếu.'], '—',
       ['Cột SL hiện 1.25 và 0.5; dòng Hợp đồng / Phụ lục dưới mỗi hàng hiện đúng số lẻ',
        'Lưu thành công (mức sàn 0.01 cho SL báo về)'])
S5.add('[YC đặt hàng mua ngoài] SL lẻ hiển thị trên chi tiết', 'P1', DATA_MN.replace('SL 2', 'SL 1.25'),
       [MENU('Mua ngoài', 'Danh sách yêu cầu đặt hàng mua ngoài'), 'Mở YCMN-1.'], '—', ['Cột SL hiện 1.25'])

# ============================================================================ VI. IN PHIẾU
S6 = Sec(6)
S6.add(tag(SC['ycg'], 'Bản in hiện đủ phần lẻ'), 'P0',
       SC['ycg']['pre'] + '\nPDH-A đã duyệt: HH01 cho KH01 SL yêu cầu 1.25, SL duyệt 0.75; HH02 đặt tồn kho SL yêu cầu 0.5, SL duyệt 0.05.',
       [SC['ycg']['menu'], 'Mở chi tiết PDH-A, bấm In.'], '—',
       ['Bản in: HH01 SL yêu cầu 1.25, SL duyệt 0.75; dòng "Đặt tồn kho" HH02 0.5 / 0.05',
        'Cột tổng SL của hàng = 1.25 (không in 1)', 'Không có ô nào in số nguyên bị làm tròn'])
for k in ('po_nk', 'po_tn'):
    s = SC[k]
    for mau in ('Cơ bản', 'Nội bộ', 'Caltex', 'Jx'):
        S6.add(tag(s, 'In yêu cầu báo giá mẫu %s hiện SL lẻ' % mau), 'P0' if mau in ('Cơ bản', 'Nội bộ') else 'P1',
               s['pre'] + '\nPO đã duyệt: HH thứ nhất SL đặt hãng 1.25 cho KH01 + Đặt tồn kho bổ sung 0.5 (Tổng SL 1.75); HH thứ hai 12.34.',
               [s['menu'], 'Mở chi tiết PO, bấm "In yêu cầu báo giá".', 'Chọn nhà cung cấp, Ngôn ngữ (lần lượt từng ngôn ngữ có sẵn), Mẫu: %s.' % mau,
                'Bấm In.'],
               'Mẫu: %s' % mau,
               ['Cột số lượng in 1.75 và 12.34' + (' ; cột số lượng quy đổi ĐVT gốc cũng giữ phần lẻ' if mau == 'Caltex' else ''),
                'Dòng TỔNG số lượng = 14.09' if mau in ('Caltex', 'Jx', 'Cơ bản') else 'Dòng khách hàng có chữ "SL đặt bổ sung: 0.5"',
                'Cột thành tiền / đơn giá giữ cách in cũ'])
S6.add(tag(SC['pi_tn'], 'Bản in PI hiện SL đặt, SL về lẻ'), 'P0',
       SC['pi_tn']['pre'] + '\nPI-T đã lưu: HH03 SL đặt 1.25 chia 2 đợt giao 0.75 + 0.5.',
       [SC['pi_tn']['menu'], 'Bấm In ở PI-T.'], '—', ['Cột SL đặt in 1.25, cột SL về in 0.75 và 0.5'])
S6.add(tag(SC['pi_nk'], 'Bản in PI nhập khẩu'), 'P2', SC['pi_nk']['pre'] + '\nPI-A đã lưu với SL về 1.25.',
       [SC['pi_nk']['menu'], 'Bấm In ở PI-A (nếu màn có nút In).'], '—',
       ['Ghi nhận kết quả: task không sửa mẫu in PI nhập khẩu — nếu in ra 1 thay vì 1.25 thì báo lại (xem mục 9)'])
S6.add('[Báo hàng về nhập khẩu] Bản in hiện SL lẻ', 'P0', DATA_NK + '\nPhiếu báo hàng về BHV-A: HH01 SL 1.25 (KH01 1.25), HH02 SL 0.5.',
       [MENU('Nhập khẩu', 'Danh sách báo hàng về'), 'Bấm In ở BHV-A.'], '—',
       ['Cột SL hàng in 1.25 và 0.5 (trước đây in "1.25" thô hoặc "1")', 'Cột SL theo từng yêu cầu / khách in 1.25'])
S6.add(tag(SC['bhv_tn'], 'Bản in hiện SL lẻ'), 'P0', SC['bhv_tn']['pre'] + '\nPhiếu báo hàng về BHV-T: HH03 SL 1.25, HH04 SL 2.',
       [SC['bhv_tn']['menu'], 'Bấm In ở BHV-T.'], '—',
       ['Cột SL in 1.25 và 2 (không in "1.00" / "2.00" thô)', 'Cột SL theo từng yêu cầu in đúng phần lẻ'])

# ============================================================================ VII. XUẤT DANH SÁCH EXCEL
S7 = Sec(7)
S7.add(tag(SC['ycg'], 'Xuất excel phiếu hiện đủ phần lẻ'), 'P0',
       SC['ycg']['pre'] + '\nPDH-A đã duyệt như ở case in (1.25 / 0.75; tồn kho 0.5 / 0.05).',
       [SC['ycg']['menu'], 'Mở chi tiết PDH-A, bấm "Xuất excel".', 'Mở tệp tải về.'], '—',
       ['Các ô SL yêu cầu / SL duyệt / tổng: 1.25, 0.75, 0.5, 0.05', 'Không ô nào bị làm tròn thành số nguyên'])
for k in ('po_nk', 'po_tn'):
    s = SC[k]
    S7.add(tag(s, 'Xuất Excel yêu cầu báo giá các mẫu'), 'P0',
           s['pre'] + '\nPO đã duyệt: HH thứ nhất Tổng SL 1.75 (gồm Đặt tồn kho bổ sung 0.5), HH thứ hai 12.34.',
           [s['menu'], 'Mở chi tiết PO, bấm "In yêu cầu báo giá".', 'Chọn nhà cung cấp, Ngôn ngữ, lần lượt Mẫu Cơ bản / Nội bộ / Caltex / Jx.',
            'Bấm Xuất Excel từng mẫu, mở tệp.'],
           'Mẫu: Cơ bản, Nội bộ, Caltex, Jx',
           ['Cột số lượng: 1.75 và 12.34 ở cả 4 mẫu, mọi ngôn ngữ',
            'Mẫu Nội bộ: dòng "SL đặt bổ sung: 0.5" (bản tiếng Anh "Quantity additional: 0.5")',
            'Mẫu Caltex / Jx: dòng tổng số lượng = 14.09'])
    S7.add(tag(s, 'Số lớn trong Excel có dấu ngăn nghìn'), 'P1',
           s['pre'] + '\nPO đã duyệt: HH thứ nhất Tổng SL 1234.56.',
           [s['menu'], 'Xuất Excel yêu cầu báo giá mẫu Cơ bản.'], '—',
           ['Ô số lượng hiện 1,234.56 (dấu phẩy ngăn nghìn, dấu chấm thập phân) — không hiện 1.234,56'])
S7.add('[YC đặt hàng mua ngoài] Xuất Excel danh sách hiện tổng SL lẻ', 'P1',
       DATA_MN.replace('SL 2', 'SL 1.25') + '\nĐăng nhập người mua.',
       [MENU('Mua ngoài', 'Danh sách yêu cầu đặt hàng mua ngoài'), 'Bấm Xuất Excel, mở tệp.'], '—',
       ['Cột tổng số lượng của YCMN-1 = 1.25 (không 1)'])

# ============================================================================ VIII. RÀNG BUỘC
S8 = Sec(8)
S8.add('[Luồng nhập khẩu] YC gốc -> YC nhập khẩu -> PO -> PI chuyển đúng SL lẻ', 'P0',
       DATA_NK + '\n' + ACC + '\nNCC1 có đơn giá HH01 = 80 USD.',
       ['S lập YC gốc: HH01 cho KH01 SL 1.25, HH02 đặt tồn kho SL 0.5; Lưu & Gửi.',
        'TP mở phiếu, giữ SL duyệt, bấm "Duyệt và gửi"; M bấm "Kế hoạch mua hàng tiếp nhận".',
        MENU('Nhập khẩu', 'Yêu cầu đặt hàng nhập khẩu') + ' Mở YC nhập khẩu sinh ra.',
        'Vào "Luồng mua nhập khẩu cần tổng hợp", lập PO từ luồng; Lưu, duyệt.',
        'Vào "PI theo NCC", lập PI từ PO.'], '—',
       ['YC nhập khẩu: SL đặt HH01 1.25, HH02 0.5',
        'PO: cột SL duyệt 1.25 / 0.5, SL đặt hãng điền sẵn 1.25 / 0.5, Tổng SL đúng',
        'PI: cột SL đặt 1.25 / 0.5'])
S8.add('[Luồng nhập khẩu] PI chia 3 đợt 0.06 + 0.57 + 0.37 không bị chặn sai', 'P0',
       SC['pi_nk']['pre'].replace('SL đặt 1.25', 'SL đặt 1'),
       [SC['pi_nk']['menu'], 'Lập PI từ PO-A; ở HH01 bấm "Thêm giao hàng" 2 lần để có 3 đợt.',
        'Nhập SL về 3 đợt: 0.06, 0.57, 0.37.', 'Bấm Lưu.'],
       ['SL đặt HH01: 1', 'SL về: 0.06 / 0.57 / 0.37'],
       ['Lưu thành công — KHÔNG hiện %s' % PI_MSG, 'Mở lại: 3 đợt giữ đúng 0.06, 0.57, 0.37; tổng SL về hiện 1'])
S8.add('[Luồng trong nước] PI chia 3 đợt 0.06 + 0.57 + 0.37 không bị chặn sai', 'P0',
       SC['pi_tn']['pre'].replace('SL đặt 1.25', 'SL đặt 1'),
       [SC['pi_tn']['menu'], 'Lập PI từ PO-T; ở HH03 bấm "Thêm giao hàng" 2 lần.', 'Nhập SL về 3 đợt: 0.06, 0.57, 0.37.', 'Bấm Lưu.'],
       ['SL đặt HH03: 1', 'SL về: 0.06 / 0.57 / 0.37'],
       ['Lưu thành công, không hiện %s' % PI_MSG, 'Mở lại giữ đúng 3 đợt'])
S8.add('[Luồng nhập khẩu] PI -> HĐ mua -> Invoice -> báo hàng về', 'P0',
       DATA_NK + '\nPI-A đã duyệt: HH01 SL PI 1.25 (2 đợt 0.75 + 0.5), đơn giá 80 USD. Có tệp PDF. Đăng nhập M.',
       ['Vào "PI theo NCC" > thẻ Chưa lập HĐ, lập HĐ-A từ PI-A với SL lập HĐ 1.25; Lưu, duyệt.',
        'Kiểm thẻ Đã lập HĐ của PI-A.', MENU('Nhập khẩu', 'Danh sách Invoice') + ' Lập Invoice từ HĐ-A với SL Invoice 0.5, đính kèm PDF; Lưu, duyệt.',
        'Lập Invoice thứ hai từ HĐ-A.', MENU('Nhập khẩu', 'Danh sách báo hàng về') + ' Lập phiếu báo hàng về từ Invoice thứ nhất.'], '—',
       ['HĐ-A: SL HĐ 1.25, Thành tiền 100 USD', 'PI-A chuyển sang thẻ Đã lập HĐ (lập đủ 1.25)',
        'Invoice 2: SL đã Invoice hiện 0.5, SL Invoice điền tối đa 0.75',
        'Báo hàng về: SL 0.5 cho KH01'])
S8.add('[Luồng nhập khẩu] Lập HĐ từng phần với SL lẻ', 'P0', SC['hd_nk']['pre'],
       [SC['hd_nk']['menu'], 'Lập HĐ thứ nhất từ PI-A với SL lập HĐ HH01 = 0.5; Lưu.', 'Lập HĐ thứ hai từ PI-A.'], '—',
       ['HĐ thứ hai: SL lập HĐ HH01 điền sẵn 0.75 (1.25 - 0.5), không vượt 0.75', 'PI-A vẫn ở thẻ Chưa lập HĐ sau HĐ thứ nhất'])
S8.add('[Luồng nhập khẩu] PLBS cộng thêm SL lẻ vào hợp đồng', 'P0', SC['plbs_nk']['pre'],
       [SC['plbs_nk']['menu'], 'Lập PLBS từ HĐ-A + PI-B với SL lập HĐ 0.75; Lưu, duyệt.', 'Lập Invoice từ HĐ-A.'], '—',
       ['PLBS lưu 0.75', 'Invoice: SL HĐ của HH01 = 2 (1.25 + 0.75), SL Invoice cho phép tới 2'])
S8.add('[Luồng nhập khẩu] PLG trừ SL lẻ khỏi hợp đồng', 'P0', SC['plg_nk']['pre'],
       [SC['plg_nk']['menu'], 'Lập PLG từ HĐ-A với SL giảm HH01 = 0.25; Lưu, duyệt.', 'Lập Invoice từ HĐ-A.'], '—',
       ['PLG lưu 0.25, Thành tiền giảm 20 USD', 'Invoice: SL Invoice HH01 tối đa 1 (1.25 - 0.25)'])
S8.add('[Luồng trong nước theo hãng] YC -> PO -> PI -> HĐ -> báo hàng về', 'P0',
       DATA_TN + '\n' + ACC + '\nĐơn giá HH03 = 2,000,000 VND.',
       ['YC gốc cho thương hiệu B2: HH03 cho KH01 SL 1.25; duyệt và tiếp nhận như luồng nhập khẩu.',
        MENU('Mua trong nước theo hãng', 'Yêu cầu đặt hàng trong nước theo hãng') + ' Mở YC trong nước sinh ra.',
        'Lập PO từ "Luồng mua trong nước theo hãng"; lập PI từ "PI theo NCC"; lập HĐ từ thẻ Chưa lập HĐ; duyệt từng phiếu.',
        MENU('Mua trong nước theo hãng', 'Phiếu báo hàng về') + ' Lập phiếu báo hàng về từ HĐ với SL 1.25.'], '—',
       ['YC trong nước lưu 1.25 (trước đây bị cắt thành 1)', 'PO / PI / HĐ chuyển nguyên 1.25, HĐ Thành tiền 2,500,000 VND',
        'Báo hàng về: SL Hợp đồng 1.25, lưu SL 1.25'])
S8.add('[Luồng trong nước theo hãng] HĐ nguyên tắc -> đơn hàng nguyên tắc', 'P1', SC['dhnt']['pre'],
       [MENU('Mua trong nước theo hãng', 'Hợp đồng nguyên tắc') + ' Mở HĐNT-1.', SC['dhnt']['menu'],
        'Lập đơn hàng nguyên tắc từ HĐNT-1 + PI-N với SL lập HĐ 1.25; Lưu.'], '—',
       ['HĐ nguyên tắc không có ô SL để sửa (SL cố định 1 — đúng thiết kế, không thuộc phạm vi)',
        'Đơn hàng nguyên tắc lưu 1.25, thành tiền 2,500,000 VND theo đơn giá nguyên tắc'])
S8.add('[Luồng trong nước tự do] YC -> PO -> PI -> HĐ -> PLBS -> báo hàng về', 'P0',
       DATA_TN.replace('B2 - hãng H2 (mua trong nước)', 'B3 - hãng H3 (mua trong nước tự do)') + '\n' + ACC,
       [MENU('Mua trong nước tự do', 'Yêu cầu đặt hàng trong nước tự do') + ' Lập YC: HH03 SL 0.5, HH04 SL 1.25; gửi, duyệt.',
        'Lập PO từ "Tổng hợp luồng mua trong nước tự do"; lập PI từ "Danh sách PI theo NCC"; lập HĐ; duyệt.',
        'Lập PLBS cho HĐ với SL 0.25.', 'Lập phiếu báo hàng về.'], '—',
       ['Mọi phiếu giữ đúng 0.5 / 1.25; PLBS 0.25', 'Báo hàng về: SL Hợp đồng HH03 = 0.75 (0.5 + 0.25)'])
S8.add('[Luồng mua ngoài] HĐ -> phụ lục -> phụ lục giảm', 'P0', DATA_MN + '\nĐơn giá HH05 = 2,000,000 VND.',
       [MENU('Mua ngoài', 'Danh sách hợp đồng mua hàng ngoài') + ' Lập HĐMN-1 từ YCMN-1 với SL lập HĐ 1.25; Lưu, duyệt.',
        MENU('Mua ngoài', 'Danh sách phụ lục hợp đồng mua hàng ngoài') + ' Lập phụ lục cho HĐMN-1.',
        MENU('Mua ngoài', 'Danh sách phụ lục giảm hợp đồng mua hàng ngoài') + ' Lập phụ lục giảm HĐMN-1 với SL giảm 0.25.'], '—',
       ['HĐMN-1 lưu 1.25, Thành tiền 2,500,000 VND', 'Phụ lục: SL lập HĐ HH05 tối đa 0.75 (2 - 1.25)',
        'Phụ lục giảm: SL Còn lại trên HĐ 1.25, lưu SL giảm 0.25, Thành tiền giảm 500,000 VND'])
S8.add('[Luồng nhập khẩu] SL còn lại / đã đặt của YC gốc sau khi lập YC con', 'P1',
       SC['ycg']['pre'] + '\nPDH-A đã tiếp nhận: HH01 SL duyệt 1.25.',
       [SC['ycg']['menu'], 'Mở chi tiết PDH-A sau khi YC nhập khẩu và PO đã lập.'], '—',
       ['Các cột SL đã đặt / còn lại (nếu có) tính trên số lẻ: đã đặt 1.25, còn lại 0'])
S8.add('[Báo hàng về nhập khẩu] Tạo phiếu với SL báo về nhỏ hơn 0.01 bị chặn', 'P2',
       DATA_NK + '\nInvoice INV-B đã duyệt: HH01 SL 0.', [MENU('Nhập khẩu', 'Danh sách báo hàng về'), 'Lập phiếu từ INV-B, bấm Lưu.'], '—',
       ['Không lưu, báo %s (mức sàn đổi từ 1 xuống 0.01)' % MIN_MSG])
S8.add('[Toàn luồng] Dữ liệu cũ là số nguyên không đổi', 'P1',
       'Các phiếu lập trước khi cập nhật (YC gốc PDH-OLD SL 3, PO-OLD Tổng SL 5, HĐ-OLD SL 2).',
       ['Mở chi tiết, Sửa (nếu được), In, Xuất Excel từng phiếu cũ.'], '—',
       ['Hiện 3 / 5 / 2 như trước (không hiện 3.00)', 'Sửa rồi lưu lại không đổi số'])

# ============================================================================ IX. PHÂN QUYỀN
S9 = Sec(9)
S9.add('[YC đặt hàng gốc] Quyền duyệt giữ nguyên', 'P0',
       PRE_D.replace('Đăng nhập tài khoản TP.', 'Tài khoản N: cùng phòng KD1, KHÔNG có quyền "Trưởng phòng duyệt yêu cầu đặt hàng".'),
       ['Đăng nhập N.', MENU_D, 'Mở PDH-A.'], '—',
       ['Không có nút "Duyệt và gửi" / "Không duyệt" (như trước khi sửa)', 'Ô SL duyệt không cho nhập'])
S9.add('[YC đặt hàng gốc] Hãng chưa phân công người mua vẫn bị chặn', 'P1',
       DATA_NK.replace('đã phân công người mua là tài khoản M', 'CHƯA phân công người mua') + '\nĐăng nhập tài khoản S.',
       [SC['ycg']['menu']] + SC['ycg']['new'] + ['Nhập SL 1.25, bấm "Lưu & Gửi".'], 'SL: 1.25',
       ['Không gửi được, thông báo %s — số lẻ không làm thay đổi kiểm tra phân công' % NOASSIGN])
S9.add('[Toàn luồng] Người không được phân công không thao tác được phiếu', 'P1',
       DATA_NK + '\nTài khoản M2: người mua, KHÔNG được phân công hãng H1.',
       ['Đăng nhập M2.', MENU('Nhập khẩu', 'Đơn hỏi hàng - PO'), 'Tìm PO của hãng H1 có SL lẻ.'], '—',
       ['Phạm vi xem / nút thao tác giống hệt trước khi sửa (task không đổi phân quyền)'])

SECTIONS = [
    ('I', 'THÊM MỚI', S1),
    ('II', 'CHỈNH SỬA', S2),
    ('III', 'DUYỆT PHIẾU', S3),
    ('IV', 'KHÔNG DUYỆT PHIẾU', S4),
    ('V', 'XEM CHI TIẾT PHIẾU MUA HÀNG', S5),
    ('VI', 'IN PHIẾU', S6),
    ('VII', 'XUẤT DANH SÁCH EXCEL', S7),
    ('VIII', 'RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC', S8),
    ('IX', 'PHÂN QUYỀN', S9),
]

MAN = '\n'.join('- %s' % x for x in [
    'Tiếp nhận đặt hàng: YC đặt hàng gốc (SL, SL đặt tồn kho; bước duyệt: SL duyệt).',
    'Nhập khẩu: YC đặt hàng nhập khẩu (SL) · PO nhập khẩu (SL đặt hãng, Đặt tồn kho bổ sung) · PI nhập khẩu (SL về từng đợt giao) · '
    'HĐ mua nhập khẩu + PLBS (SL lập HĐ) · PLG (SL giảm) · Invoice (SL Invoice) · Báo hàng về (SL lấy từ Invoice, chỉ hiển thị + in).',
    'Mua trong nước theo hãng / tự do: YC đặt hàng trong nước (SL) · PO (SL đặt hãng, Đặt tồn kho bổ sung) · PI (SL về) · '
    'HĐ mua + PLBS + Đơn hàng nguyên tắc (SL lập HĐ) · Phiếu báo hàng về (SL).',
    'Mua ngoài: HĐ mua hàng ngoài + Phụ lục (SL lập HĐ) · Phụ lục giảm (SL giảm) · YC mua ngoài (Xuất Excel).'])

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Redmine #12195: ở các phiếu của luồng Mua hàng, ô "số lượng đặt" và "SL duyệt" cho nhập số thập phân tối đa 2 chữ số lẻ '
     '(kể cả số nhỏ hơn 1, vd 0.5, 0.05, 1.25) thay vì chỉ số nguyên. Màn hình, bản in và file Excel hiện đủ phần lẻ.\n'
     'Áp cho 4 luồng trong menu Mua hàng: Nhập khẩu (có Invoice, PLG), Mua trong nước theo hãng, Mua trong nước tự do, Mua ngoài.'),
    ('2. Đối tượng được tính / hiển thị',
     'Các màn và ô được sửa (cột Chức năng ghi tên màn trong ngoặc vuông):\n' + MAN + '\n'
     'Hiển thị số lẻ ở: lưới chi tiết, dòng tổng SL, bản in (YC gốc, yêu cầu báo giá PO 4 mẫu Cơ bản / Nội bộ / Caltex / Jx, '
     'PI trong nước, báo hàng về nhập khẩu và trong nước), Excel (YC gốc, yêu cầu báo giá PO 4 mẫu, danh sách YC mua ngoài).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- KHÔNG đổi: SL khuyến mãi, SL bảo hành, SL chênh lệch, các ô đơn giá / thành tiền / thuế (vẫn như cũ).\n'
     '- HĐ nguyên tắc: SL cố định 1 (hợp đồng theo đơn giá), không có ô SL để sửa.\n'
     '- Không đổi phân quyền, trạng thái, luồng duyệt, mức trần cũ (SL duyệt không vượt SL yêu cầu…) — chỉ cho các trần đó nhận số lẻ.\n'
     '- Ngoài phạm vi (lỗi có sẵn): PLG nhập khẩu giảm dòng "Tồn kho" báo lỗi hệ thống — không thuộc task này.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Không áp dụng — task không đổi bộ lọc / tìm kiếm của các màn.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Luồng nhập khẩu: YC gốc -> YC nhập khẩu -> PO -> PI (chia nhiều đợt giao) -> HĐ mua (+ PLBS / PLG) -> Invoice -> báo hàng về.\n'
     'Luồng trong nước: YC gốc -> YC trong nước -> PO -> PI -> HĐ mua / đơn hàng nguyên tắc (+ PLBS) -> phiếu báo hàng về.\n'
     'Luồng mua ngoài: YC mua ngoài -> HĐ mua hàng ngoài -> phụ lục / phụ lục giảm.\n'
     'SL lẻ ở phiếu trước được chuyển nguyên sang phiếu sau; SL còn lại = SL phiếu trước - SL đã lập (tính trên số lẻ).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Mọi tổng SL (tổng theo hàng, theo khách, theo đợt giao) được làm tròn 2 chữ số: 0.1 + 0.2 hiện 0.3, 0.06 + 0.57 + 0.37 = 1.\n'
     '- Tổng SL PO = SL đặt hãng các khách + Đặt tồn kho bổ sung (cộng SỐ, không nối chuỗi).\n'
     '- PI: tổng SL về các đợt phải bằng SL đặt (so sau khi làm tròn 2 số), lệch thì chặn ' + PI_MSG + '.'),
    ('7. Phân quyền cấp',
     'Không đổi. Quyền liên quan giữ như cũ: "Trưởng phòng duyệt yêu cầu đặt hàng" (nút Duyệt và gửi / Không duyệt ở YC gốc); '
     'các phiếu PO / PI / HĐ / Invoice kiểm theo phân công người mua của thương hiệu - hãng. Nhóm PHÂN QUYỀN chỉ kiểm hồi quy.'),
    ('8. Cách tính các ô thống kê',
     '- Thành tiền = SL (đủ 2 số lẻ) × đơn giá; vd 1.25 × 80 USD = 100 USD; 0.05 × 2,000,000 = 100,000 VND.\n'
     '- Ô nhập: gõ 3 số lẻ thì tự làm tròn 2 số khi rời ô (1.255 -> 1.25, 1.256 -> 1.26, 0.125 -> 0.13).\n'
     '- Mức sàn: YC gốc, YC nhập khẩu, Invoice, HĐ (khi sửa), HĐ trong nước / đơn hàng nguyên tắc / PLBS trong nước, báo hàng về '
     'nhập khẩu: nhỏ nhất 0.01; 0 hoặc trống bị chặn ' + MIN_MSG + '. PO (SL đặt hãng, Đặt tồn kho bổ sung), PLG trong nước / mua '
     'ngoài, phiếu báo hàng về trong nước: giữ quy tắc cũ cho phép 0.\n'
     '- Mức trần (tự kéo về trần, không báo lỗi — hành vi cũ): SL duyệt <= SL yêu cầu; SL về <= SL đặt; SL lập HĐ <= SL PI còn lại; '
     'SL Invoice <= SL HĐ - SL đã Invoice; SL giảm <= SL hợp đồng / còn lại; SL báo về <= SL Hợp đồng; số âm -> 0.'),
    ('9. Ghi chú đọc bảng',
     '- NGOẠI LỆ "mỗi màn 1 file": task sửa MỘT loại trường trên ~20 màn có sẵn nên gộp 1 file; tên màn ghi ở đầu cột Chức năng '
     '"[Tên màn] …" (cột Module chỉ ghi ở case đầu nhóm theo khuôn chuẩn). Chỉ có các nhóm liên quan; nhóm Tìm kiếm, Xoá, Khoá, '
     'Lịch sử… bỏ vì task không đổi.\n'
     '- BẪY DẤU THẬP PHÂN: ô nhập là ô SỐ, gõ dấu CHẤM (1.25). Gõ dấu phẩy "1,25" trình duyệt không nhận -> coi như 0 / trống. '
     'Ô nhập KHÔNG có dấu ngăn nghìn (gõ 1234.56); chỗ hiển thị, bản in, Excel dùng chuẩn quốc tế 1,234.56.\n'
     '- Hiển thị BỎ số 0 thừa: 1.50 hiện 1.5, 2.00 hiện 2 — đúng thiết kế, không phải mất phần lẻ.\n'
     '- Câu báo lỗi mức sàn ghi "Phải lớn hơn 0.01." nhưng 0.01 VẪN hợp lệ (câu chữ có sẵn của hệ thống). Để trống ô cũng ra câu này '
     '(ô trống được hiểu là 0), không phải "Bắt buộc phải nhập".\n'
     '- Nhập vượt trần: ô tự kéo về trần, không báo đỏ — là hành vi cũ của các màn này, giữ nguyên.\n'
     '- Ô "YC đặt hàng trong nước" (lập trực tiếp) chưa đổi bước nhập (mũi tên tăng 1) và không có mức sàn ở máy chủ: QA ghi kết quả '
     'thực tế. Phần lưu số lẻ đã sửa (trước đây 1.25 lưu thành 1). Môi trường mới cần cập nhật cấu trúc dữ liệu trước khi test.\n'
     '- Phiếu báo hàng về mua ngoài, bản in PI nhập khẩu: task không sửa — các case ghi "ghi nhận kết quả thực tế".\n'
     '- Số liệu mẫu (PDH-A, PO-A, PI-A, HĐ-A…) là tên giả lập: QA lập phiếu thật theo Tiền điều kiện rồi thay mã.'),
]

if __name__ == '__main__':
    ids = [(s.idx, tc[0]) for _, _, s in SECTIONS for tc in s]
    assert len(ids) == len(set(ids)), 'Trùng mã TC'
    total = len(ids)
    p0 = sum(1 for _, _, s in SECTIONS for tc in s if tc[2] == 'P0')
    print('Tong %d TC, P0 %d (%.0f%%)' % (total, p0, 100.0 * p0 / total))
    for r, t, s in SECTIONS:
        print('  %s. %s: %d' % (r, t, len(s)))
    per = Counter()
    for _, _, s in SECTIONS:
        for tc in s:
            per[tc[1].split(']')[0].lstrip('[') if tc[1].startswith('[') else '(khác)'] += 1
    print('Theo màn:')
    for k, v in per.most_common():
        print('  %s: %d' % (k, v))
    build_chuan(output_file=OUT, sheet_name='Trang tính1',
                feature_name='SL đặt / SL duyệt số thập phân - Mua hàng (#12195) - Cập nhật ngày 18/11/2026',
                module_name='Mua hàng - SL thập phân', description_block=DESCRIPTION_BLOCK,
                sections=[(r, t, list(s)) for r, t, s in SECTIONS], loai='phieu')
