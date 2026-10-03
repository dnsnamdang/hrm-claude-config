# -*- coding: utf-8 -*-
"""Sinh testcase PHIA ERP (he thong cu TanPhatDev) cho 2 man Khai bao dau ky cong no:

  - "testcase ERP - Khai bao dau ky cong no.xlsx"
  - "testcase ERP - Khai bao dau ky cong no nha cung cap.xlsx"

Muc dich (user yeu cau 02/10/2026): de nguoi dung / tester HIEU THAO TAC TREN ERP — man, nut, cua so,
cau thong bao dung nhu ERP dang chay. KHONG phai testcase man HRM (ban HRM: gen_testcase.py).

Ket qua mong doi = hanh vi ERP HIEN TAI (doc tu code ERP ngay 01-02/10/2026). Cho nao ERP dang co
loi thi ghi them dong "Lưu ý (hành vi hiện tại của ERP): ..." de nguoi doc khong hieu nham la dung.
Ngon ngu NGHIEP VU — khong dung thuat ngu code.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, '..', '..', '..', '.claude', 'skills',
                                'testcase-documenter', 'assets'))
from tc_engine import build  # noqa: E402


def nl(*lines):
    return '\n'.join(lines)


SCOPE_PERMS = [
    ('Xem tất cả công nợ đầu kỳ', 'mọi khai báo của mọi công ty; khối lọc có ô Công ty, Phòng ban, Bộ phận'),
    ('Xem tất cả công nợ đầu kỳ của công ty', 'khai báo thuộc công ty của người đăng nhập'),
    ('Xem tất cả công nợ đầu kỳ của phòng ban', 'khai báo thuộc các phòng ban người đăng nhập được giao quản lý'),
    ('Xem tất cả công nợ đầu kỳ của bộ phận', 'khai báo thuộc các bộ phận người đăng nhập được giao quản lý'),
]

KH = dict(
    title='Khai báo đầu kỳ công nợ', module='ERP - Khai báo đầu kỳ công nợ KH',
    page_title='Công nợ đầu kỳ theo khách hàng - hợp đồng',
    menu='Kế toán > nhóm Khai báo đầu kỳ > Khai báo đầu kỳ công nợ',
    menu2='Kế toán > Kế toán công nợ > nhóm Khách hàng > Công nợ đầu kỳ theo khách hàng - hợp đồng',
    obj='khách hàng', Obj='Khách hàng', form_obj_label='Khách hàng/Nhà cung cấp',
    modal_add='Thêm mới công nợ đầu kỳ', modal_edit='Chỉnh công nợ đầu kỳ',
    picker_btn='Hợp đồng/đơn hàng', picker_title='Hợp đồng/Đơn hàng',
    code_col='Mã', code_sample='TPE.CNĐKHĐ.00001', code_rule='<mã công ty>.CNĐKHĐ.<số 5 chữ số>',
    account_no='1311', account='1311 - Phải thu của khách hàng ngắn hạn',
    obj_sample='75TPHXCH-2 - CÔNG TY CỔ PHẦN KIM LONG MOTORS HUẾ', obj_code='75TPHXCH-2',
    contract_sample='HĐ_TPE_HN_KD3_26_0548_HD2605-0004',
    msg_add='Thêm công nợ thành công!', msg_edit='Cập nhật công nợ thành công!',
    msg_del='Xóa công nợ thành công!', msg_no_obj='Chưa chọn khách hàng',
    file_export='danh_sach_cong_no_dau_ky_khach_hang_hop_dong.xlsx',
    export_title='DANH SÁCH CÔNG NỢ ĐẦU KỲ THEO KHÁCH HÀNG - HỢP ĐỒNG',
    sample_file='ImportExcel_Congnodaukikhachhang.xlsx',
    is_ncc=False, out='testcase ERP - Khai bao dau ky cong no.xlsx',
)
NCC = dict(
    title='Khai báo đầu kỳ công nợ nhà cung cấp', module='ERP - Khai báo đầu kỳ công nợ NCC',
    page_title='Khai báo công nợ đầu kỳ nhà cung cấp',
    menu='Kế toán > nhóm Khai báo đầu kỳ > Khai báo đầu kỳ công nợ nhà cung cấp',
    menu2=None,
    obj='nhà cung cấp', Obj='Nhà cung cấp', form_obj_label='Nhà cung cấp',
    modal_add='Thêm mới công nợ đầu kỳ nhà cung cấp', modal_edit='Chỉnh công nợ đầu kỳ nhà cung cấp',
    picker_btn='Chọn Hợp đồng', picker_title='Chọn hợp đồng nhà cung cấp',
    code_col='Số phiếu', code_sample='TPE_DKNCC_00318', code_rule='<mã công ty>_DKNCC_<số 5 chữ số>',
    account_no='3311', account='3311-Phải trả cho người bán ngắn hạn',
    obj_sample='FLY - ZHONGSHAN EAGLE-FLY ELECTRICAL APPLIANCE CO.,LTD', obj_code='FLY',
    contract_sample='FLY 0726 HP-ANNEX 01',
    msg_add='Thêm công nợ thành công!', msg_edit='Cập nhật công nợ thành công!',
    msg_del='Xóa công nợ nhà cung cấp thành công!', msg_no_obj='Chưa chọn nhà cung cấp',
    file_export='danh_sach_cong_no_dau_ky_ncc.xlsx',
    export_title='DANH SÁCH CÔNG NỢ ĐẦU KỲ THEO NHÀ CUNG CẤP - HỢP ĐỒNG',
    sample_file='ImportExcel_Congnodaukinhacungcap.xlsx',
    is_ncc=True, out='testcase ERP - Khai bao dau ky cong no nha cung cap.xlsx',
)


# =====================================================================================================
def description(c):
    ncc = c['is_ncc']
    d1 = nl(
        'Màn hình "{t}" trên ERP (tiêu đề trang: "{p}") dùng để nhập SỐ DƯ CÔNG NỢ ĐẦU KỲ cho từng hợp '
        'đồng của một {o}, làm số mở đầu cho sổ chi tiết công nợ và các báo cáo công nợ.'.format(
            t=c['title'], p=c['page_title'], o=c['obj']),
        'Mỗi dòng khai báo ghi MỘT bút toán vào sổ chi tiết tài khoản (Nợ hoặc Có tài khoản đã chọn, '
        'thường là {a}), ngày hạch toán = "Ngày tính công nợ" trong cấu hình chung (hiện 01/08/2025).'.format(a=c['account_no']),
        'Thao tác chính: bấm "Tạo mới" mở cửa sổ "{m}", rồi chọn {o}, rồi bấm "{b}" chọn hợp đồng (bấm vào '
        'dòng là thêm), rồi mỗi dòng chọn Tài khoản, chọn Dư nợ / Dư có, nhập Công nợ{cur}, rồi bấm "Lưu". '
        'Mỗi dòng hợp đồng thành một khai báo riêng, mã dạng {r}.'.format(
            m=c['modal_add'], o=c['obj'], b=c['picker_btn'], r=c['code_rule'],
            cur=', chọn Loại tiền và nhập Tỷ giá' if ncc else ''),
        'Ngoài ra: Sửa (cửa sổ "{e}"), Xóa, Import excel, In, Xuất excel.'.format(e=c['modal_edit']),
        'Đường dẫn: ' + c['menu'] + ('.\nLối vào thứ hai: ' + c['menu2'] + '.' if c['menu2'] else '.'))

    d2 = nl(
        'Danh sách hiển thị theo quyền xem (xét lần lượt, gặp quyền nào trước dùng quyền đó; dùng chung '
        'cho cả màn khách hàng và nhà cung cấp):',
        *['- "%s": %s.' % p for p in SCOPE_PERMS],
        '- Không có quyền nào ở trên: chỉ khai báo do chính mình tạo.',
        'Công ty / phòng ban / bộ phận của khai báo = của NGƯỜI LẬP HỢP ĐỒNG.',
        'Cửa sổ chọn hợp đồng: ' + (
            'ô "Loại hợp đồng" có 14 lựa chọn (Hợp đồng hãng, Hợp đồng, Đơn hàng, Hợp đồng nguyên tắc, '
            'Hợp đồng thúc đẩy bán, Đơn hàng thúc đẩy bán, Phụ lục bổ sung, Phụ lục HĐNT, Hợp đồng gói '
            'dịch vụ, Hợp đồng dự án, Hợp đồng đầu kỳ, Hợp đồng mua nước ngoài, Hợp đồng mua ngoài, Hợp '
            'đồng mua trong nước). Để trống = chỉ hợp đồng bán (Đã duyệt / Có hiệu lực) của khách hàng.'
            if not ncc else
            '2 tab "HĐ Nhà cung cấp hiện tại" và "HĐ Nhà cung cấp khác"; gộp hợp đồng mua nước ngoài, '
            'mua trong nước (cũ và mới), hợp đồng mua đầu kỳ; MỌI trạng thái.'),
        'Danh sách tài khoản trên cửa sổ: ' + (
            'mọi tài khoản chi tiết đang hoạt động.' if not ncc else
            'tài khoản chi tiết đang hoạt động có đánh dấu "Theo dõi công nợ".'))

    d3 = nl(
        '- Khai báo ngoài phạm vi quyền xem không hiện trong danh sách.',
        ('- Người không có quyền "Quản lý công nợ đầu kỳ" không vào được màn (trang báo không tìm thấy).'
         if not ncc else
         '- Màn KHÔNG chặn quyền xem. Nút "Tạo mới" chỉ hiện với quyền "Khai báo thêm công nợ đầu kỳ nhà '
         'cung cấp"; nút Sửa / Xóa chỉ hiện khi có quyền sửa / xoá VÀ hợp đồng + tài khoản đó chưa có '
         'chứng từ nào khác ghi sổ.'),
        ('- Nút Sửa và Xóa LUÔN hiện trên mọi dòng (không xét đã phát sinh chứng từ hay chưa).' if not ncc else
         '- Trong cửa sổ chọn hợp đồng: hợp đồng đã khai báo cho nhà cung cấp này bấm vào sẽ báo "Hợp đồng đã được chọn.".'))

    d4 = nl(
        'Ô "Từ ngày" / "Đến ngày" lọc theo NGÀY TẠO khai báo.',
        '"Ngày tính công nợ" không lọc được và không hiện trên lưới.')

    d5 = nl(
        'Một lần lập = 1 {o} × nhiều hợp đồng; mỗi dòng lưu thành 1 khai báo (1 mã, 1 bút toán).'.format(o=c['obj']),
        'Lưới danh sách: ' + (
            'STT, Mã, Tài khoản, Khách hàng, Loại hợp đồng, Mã hợp đồng, Dư nợ, Dư có, Người tạo, Ngày '
            'tạo, Người sửa, Ngày sửa, Hành động.' if not ncc else
            'STT, Số phiếu, Tài khoản, Nhà cung cấp, Số hợp đồng, Người lập hợp đồng, Loại tiền, Dư nợ, '
            'Dư có, Người tạo, Ngày tạo, Người sửa, Ngày sửa, Hành động.'),
        'Cửa sổ Sửa chỉ có 1 dòng; ' + c['obj'] + ' bị khoá, không chọn lại hợp đồng.')

    d6 = nl(
        '- Cùng {o} + hợp đồng + tài khoản chỉ khai báo một lần khi Thêm mới.'.format(o=c['obj']),
        '- Công nợ tối thiểu 1. Dư nợ ghi Nợ tài khoản, Dư có ghi Có tài khoản.',
        ('- Khai báo khách hàng luôn là VNĐ, tỷ giá 1.' if not ncc else
         '- Quy đổi VND ghi sổ = Công nợ × Tỷ giá. Chọn VNĐ thì Tỷ giá = 1 và ô bị khoá. Tỷ giá tối thiểu 1.'),
        '- Sửa / Xóa khai báo thì bút toán trong sổ sửa / xoá theo.')

    d7 = nl(
        ('- "Quản lý công nợ đầu kỳ": vào màn và làm mọi thao tác.' if not ncc else
         '- "Khai báo thêm công nợ đầu kỳ nhà cung cấp": nút Tạo mới.\n'
         '- "Khai báo sửa công nợ đầu kỳ nhà cung cấp": nút Sửa.\n'
         '- "Khai báo xoá công nợ đầu kỳ nhà cung cấp": nút Xóa.'),
        '- Phạm vi xem: ' + '; '.join('"%s"' % p[0] for p in SCOPE_PERMS) + '.')

    d8 = nl(
        'Cột "Dư nợ" chỉ có số khi khai báo là Dư nợ, cột "Dư có" chỉ có số khi là Dư có; cột còn lại trống.',
        'Dòng "Showing ... of N" / "Hiển thị ... trên N" dưới lưới: N là tổng khai báo khớp bộ lọc và quyền.')

    d9 = nl(
        '- Nút tìm kiếm và làm mới của khối lọc chỉ là biểu tượng (kính lúp và mũi tên vòng).',
        '- Các mục "Lưu ý (hành vi hiện tại của ERP)" trong file là những điểm ERP đang chạy chưa chuẩn; '
        'người test đánh kết quả theo đúng hành vi đang thấy, KHÔNG coi là lỗi mới.',
        '- Sau mỗi lần Lưu / Sửa / Xóa có thể mở báo cáo "Sổ chi tiết công nợ ' +
        ('phải thu khách hàng' if not ncc else 'phải trả nhà cung cấp') + '" để thấy bút toán tương ứng.')

    return [
        ('1. Mục đích tính năng', d1), ('2. Đối tượng được tính / hiển thị', d2),
        ('3. Đối tượng bị ẩn / không tính', d3), ('4. Bộ lọc thời gian áp dụng cho', d4),
        ('5. Cấu trúc dữ liệu / cây phân cấp', d5), ('6. Quy tắc cộng dồn / deduplicate', d6),
        ('7. Phân quyền cấp', d7), ('8. Cách tính các ô thống kê', d8), ('9. Ghi chú đọc bảng', d9),
    ]


# =====================================================================================================
def role_tcs(c):
    ncc = c['is_ncc']
    menu = c['menu']
    tcs = []
    if not ncc:
        tcs += [
            ('00', 'Không có quyền "Quản lý công nợ đầu kỳ" thì không vào được màn', 'P0',
             'Tài khoản A không có quyền "Quản lý công nợ đầu kỳ".',
             nl('1. Đăng nhập ERP bằng A.', '2. Vào ' + menu + '.'), '—',
             nl('- Không vào được màn, hiện trang báo không tìm thấy / không có quyền.')),
            ('01', 'Có quyền "Quản lý công nợ đầu kỳ" dùng được mọi chức năng', 'P0',
             'Tài khoản B có "Quản lý công nợ đầu kỳ" và "Xem tất cả công nợ đầu kỳ của công ty".',
             nl('1. Đăng nhập bằng B.', '2. Vào ' + menu + '.'), '—',
             nl('- Hiện lưới khai báo của công ty B.', '- Thanh công cụ có: Tạo mới, In, Xuất excel, Import excel.',
                '- Mỗi dòng có nút Sửa (bút chì) và Xóa (dấu x đỏ).')),
        ]
    else:
        tcs += [
            ('00', 'Không có quyền nào vẫn vào được màn', 'P0',
             'Tài khoản A không có quyền nào của nhóm khai báo đầu kỳ; A đã tạo 2 khai báo.',
             nl('1. Đăng nhập bằng A.', '2. Vào ' + menu + '.'), '—',
             nl('- Màn mở được, chỉ thấy 2 khai báo do A tạo.', '- KHÔNG có nút Tạo mới; dòng không có Sửa / Xóa.',
                '- Vẫn có In, Xuất excel, Import excel.')),
            ('01', 'Quyền "Khai báo thêm công nợ đầu kỳ nhà cung cấp"', 'P0', 'Tài khoản B chỉ có quyền thêm.',
             nl('1. Đăng nhập bằng B, vào ' + menu + '.'), '—',
             nl('- Có nút Tạo mới; dòng không có Sửa / Xóa.')),
            ('02', 'Quyền "Khai báo sửa công nợ đầu kỳ nhà cung cấp"', 'P0',
             'Tài khoản C chỉ có quyền sửa; khai báo X chưa có chứng từ khác.',
             nl('1. Đăng nhập bằng C, vào màn.', '2. Quan sát dòng X.'), '—',
             nl('- Dòng X có nút Sửa, không có Xóa; không có nút Tạo mới.')),
            ('03', 'Quyền "Khai báo xoá công nợ đầu kỳ nhà cung cấp"', 'P0',
             'Tài khoản D chỉ có quyền xoá; khai báo X chưa có chứng từ khác.',
             nl('1. Đăng nhập bằng D, vào màn.', '2. Quan sát dòng X.'), '—',
             nl('- Dòng X có nút Xóa, không có Sửa.',
                '- Lưu ý (hành vi hiện tại của ERP): quyền chỉ dùng để ẨN nút; nếu biết đường dẫn vẫn sửa / xoá được '
                '(dành cho tester kỹ thuật kiểm thêm).')),
        ]
    for i, (p, scope) in enumerate(SCOPE_PERMS):
        tcs.append(('%02d' % len(tcs), 'Phạm vi xem: "%s"' % p, 'P0' if i < 2 else 'P1',
                    'Tài khoản E%d chỉ có quyền phạm vi "%s"%s.' % (i + 1, p, '' if ncc else ' (kèm "Quản lý công nợ đầu kỳ")'),
                    nl('1. Đăng nhập bằng E%d.' % (i + 1), '2. Vào ' + menu + ', đếm số dòng.'), '—',
                    nl('- Thấy ' + scope + '.', '- Công ty / phòng ban / bộ phận tính theo người lập hợp đồng.')))
    tcs.append(('%02d' % len(tcs), 'Không có quyền phạm vi: chỉ thấy khai báo mình tạo', 'P0',
                'Tài khoản F%s; F tạo 3 khai báo.' % ('' if ncc else ' có "Quản lý công nợ đầu kỳ" nhưng không có quyền phạm vi'),
                nl('1. Đăng nhập bằng F, vào màn.'), '—',
                nl('- Chỉ hiện 3 khai báo của F.', '- Khối lọc không có ô Công ty / Phòng ban.')))
    return tcs


# =====================================================================================================
def sections(c):
    ncc = c['is_ncc']
    menu, o, O = c['menu'], c['obj'], c['Obj']

    S1 = [
        ('001', 'Vào màn qua menu', 'P0', 'Tài khoản B đủ quyền.',
         nl('1. Đăng nhập ERP.', '2. Mở menu Kế toán.', '3. Nhóm Khai báo đầu kỳ, bấm "' + c['title'] + '".'), '—',
         nl('- Trang có tiêu đề "' + c['page_title'] + '".', '- Lưới danh sách hiện ngay, khai báo mới nhất ở trên cùng.')),
        ('002', 'Cột của lưới danh sách', 'P0', '—', nl('1. Đọc tiêu đề cột.'), '—',
         nl('- ' + ('STT, Mã, Tài khoản, Khách hàng, Loại hợp đồng, Mã hợp đồng, Dư nợ, Dư có, Người tạo, Ngày tạo, Người sửa, Ngày sửa, Hành động.'
                    if not ncc else
                    'STT, Số phiếu, Tài khoản, Nhà cung cấp, Số hợp đồng, Người lập hợp đồng, Loại tiền, Dư nợ, Dư có, Người tạo, Ngày tạo, Người sửa, Ngày sửa, Hành động.'),
            '- Tài khoản dạng "số - tên", ' + O + ' dạng "mã - tên".',
            '- Ngày tạo / Ngày sửa dạng dd/mm/yyyy giờ:phút:giây.')),
        ('003', 'Số hợp đồng trên lưới là đường dẫn', 'P1', 'Có khai báo gắn hợp đồng ' + ('đầu kỳ' if not ncc else 'mua') + '.',
         nl('1. Bấm vào số hợp đồng ở cột "' + ('Mã hợp đồng' if not ncc else 'Số hợp đồng') + '".'), '—',
         nl('- Mở trang hợp đồng tương ứng ở tab mới.')),
        ('004', 'Dư nợ / Dư có hiển thị đúng cột', 'P1', 'Có 1 khai báo Dư nợ 10,125,000 và 1 khai báo Dư có 25,363,563.',
         nl('1. Tìm 2 khai báo.'), '—',
         nl('- Khai báo Dư nợ: số ở cột Dư nợ, cột Dư có trống.', '- Khai báo Dư có: ngược lại.'
            + ('\n- Màn nhà cung cấp hiện 2 chữ số thập phân (vd 1,720,895.64) và cột Loại tiền (VNĐ, USD…).' if ncc else ''))),
    ]
    if c['menu2']:
        S1.append(('005', 'Lối vào thứ hai', 'P1', '—', nl('1. Vào ' + c['menu2'] + '.'), '—',
                   nl('- Mở cùng màn "' + c['page_title'] + '".', '- Cùng số khai báo như khi vào từ nhóm Khai báo đầu kỳ.')))
        S1.append(('006', 'Mở màn kèm mã phiếu từ báo cáo', 'P2', 'Có khai báo ' + c['code_sample'] + '.',
                   nl('1. Từ sổ chi tiết công nợ phải thu khách hàng, bấm vào chứng từ là khai báo đầu kỳ.'), '—',
                   nl('- Mở màn Khai báo đầu kỳ công nợ, ô "Mã phiếu" tự điền mã đó và lưới chỉ còn khai báo đó.')))

    filters = ([('Khách hàng', 'gõ tên/mã rồi chọn'), ('Tài khoản', 'chọn'), ('Mã hợp đồng', 'gõ'), ('Mã phiếu', 'gõ ĐÚNG NGUYÊN mã'),
                ('Người tạo', 'gõ rồi chọn'), ('Người sửa', 'gõ rồi chọn'), ('Số tiền từ / Số tiền đến', 'nhập số')]
               if not ncc else
               [('Nhà cung cấp', 'gõ tên/mã rồi chọn'), ('Tài khoản', 'chọn'), ('Số hợp đồng', 'gõ'), ('Người lập HĐ', 'gõ rồi chọn'),
                ('Người tạo', 'gõ rồi chọn'), ('Người sửa', 'gõ rồi chọn')])
    S2 = [
        ('001', 'Các ô lọc của màn', 'P1', '—', nl('1. Quan sát khối lọc phía trên lưới.'), '—',
         nl('- Có các ô: ' + ', '.join(f[0] for f in filters) + ', Công ty, Phòng ban, Bộ phận (theo quyền), Từ ngày, Đến ngày.',
            '- Có 2 nút biểu tượng: kính lúp (tìm kiếm) và mũi tên vòng (làm mới).')),
        ('002', 'Lọc theo ' + O, 'P0', O + ' ' + c['obj_sample'] + ' có khai báo.',
         nl('1. Ô "' + O + '" gõ "' + c['obj_code'] + '", chọn trong gợi ý.', '2. Bấm kính lúp.'), O + ': ' + c['obj_code'],
         nl('- Lưới chỉ còn khai báo của ' + o + ' đó.')),
        ('003', 'Lọc theo Tài khoản', 'P1', '—', nl('1. Ô Tài khoản chọn ' + c['account_no'] + '.', '2. Bấm kính lúp.'), '—',
         nl('- Chỉ còn khai báo tài khoản ' + c['account_no'] + '.')),
        ('004', 'Lọc theo ' + ('Mã hợp đồng' if not ncc else 'Số hợp đồng'), 'P1', 'Có khai báo gắn hợp đồng ' + c['contract_sample'] + '.',
         nl('1. Gõ một phần số hợp đồng.', '2. Bấm kính lúp.'), '—',
         nl('- Ra khai báo có số hợp đồng chứa chuỗi đã gõ.',
            '- Lưu ý (hành vi hiện tại của ERP): ' + ('không tìm được khai báo gắn hợp đồng dịch vụ bảo hành - sửa chữa hoặc hợp đồng mua trong nước (mới).'
                                                     if not ncc else 'không tìm được khai báo gắn hợp đồng mua trong nước (mới).'))),
    ]
    if not ncc:
        S2 += [
            ('005', 'Lọc theo Mã phiếu phải gõ đủ mã', 'P1', 'Có khai báo ' + c['code_sample'] + '.',
             nl('1. Ô Mã phiếu gõ "00001", bấm kính lúp.', '2. Gõ đủ "' + c['code_sample'] + '", bấm kính lúp.'), '—',
             nl('- Gõ một phần: không ra kết quả.', '- Gõ đủ mã: ra đúng 1 khai báo.')),
            ('006', 'Lọc theo Số tiền từ / đến', 'P1', 'Có khai báo 1,500,000 và 10,125,000.',
             nl('1. Số tiền từ 1,000,000; Số tiền đến 5,000,000.', '2. Bấm kính lúp.'), '—',
             nl('- Chỉ còn khai báo có số tiền trong khoảng (tính cả 2 đầu).')),
        ]
    else:
        S2.append(('005', 'Lọc theo Người lập HĐ', 'P2', 'Có khai báo của hợp đồng do Nguyễn Thị Ngoan lập.',
                   nl('1. Ô "Người lập HĐ" chọn Nguyễn Thị Ngoan, bấm kính lúp.'), '—',
                   nl('- Chỉ còn khai báo có Người lập hợp đồng là người đó.',
                      '- Lưu ý: màn nhà cung cấp KHÔNG có ô lọc Mã phiếu và Số tiền.')))
    n = len(S2)
    S2 += [
        ('%03d' % (n + 1), 'Lọc theo Người tạo / Người sửa', 'P2', '—', nl('1. Chọn Người tạo, bấm kính lúp.', '2. Xoá, chọn Người sửa, bấm kính lúp.'), '—',
         nl('- Chỉ còn khai báo do người đó tạo / sửa lần cuối.')),
        ('%03d' % (n + 2), 'Lọc theo Từ ngày / Đến ngày', 'P1', 'Có 1 khai báo tạo ngày 23/12/2025.',
         nl('1. Từ ngày 01/12/2025, Đến ngày 31/12/2025.', '2. Bấm kính lúp.'), '—',
         nl('- Ra khai báo tạo trong khoảng, tính theo ngày tạo.')),
        ('%03d' % (n + 3), 'Lọc theo Công ty / Phòng ban', 'P1', 'Tài khoản có quyền xem tất cả.',
         nl('1. Chọn Công ty, Phòng ban.', '2. Bấm kính lúp.'), '—',
         nl('- Chỉ còn khai báo thuộc công ty / phòng ban đã chọn.',
            '- Lưu ý (hành vi hiện tại của ERP): chọn Bộ phận KHÔNG lọc thêm.')),
        ('%03d' % (n + 4), 'Làm mới', 'P1', 'Đang lọc nhiều điều kiện.', nl('1. Bấm nút mũi tên vòng.'), '—',
         nl('- Các ô lọc về trống, lưới hiện lại toàn bộ.')),
    ]

    picker_cols = ('STT, Loại hợp đồng, Số hợp đồng, Khách hàng, Tổng thanh toán, Người lập' if not ncc
                   else 'STT, Số hợp đồng, Ngày lập, Người lập')
    S3 = [
        ('001', 'Mở cửa sổ Thêm mới', 'P0', 'Tài khoản có quyền thêm.', nl('1. Bấm "Tạo mới".'), '—',
         nl('- Cửa sổ "' + c['modal_add'] + '".', '- Ô "' + c['form_obj_label'] + ' (*)", placeholder "Chọn ' + o + '".',
            '- Nút "' + c['picker_btn'] + '".',
            '- Bảng cột: ' + ('STT, Loại, Số hợp đồng, Tài khoản, Công nợ' if not ncc else
                              'STT, Số hợp đồng mua, Tài khoản, Loại tiền (*), Tỷ giá (*), Công nợ') + '.',
            '- Chân cửa sổ: Lưu (xanh lá), Hủy (đỏ).')),
        ('002', 'Chưa chọn ' + o + ' mà bấm chọn hợp đồng', 'P0', '—', nl('1. Bấm "' + c['picker_btn'] + '" khi chưa chọn ' + o + '.'), '—',
         nl('- Thông báo vàng góc màn hình: "' + c['msg_no_obj'] + '".', '- Không mở cửa sổ chọn hợp đồng.')),
        ('003', 'Chọn ' + o, 'P1', '—', nl('1. Ô ' + c['form_obj_label'] + ' gõ "' + c['obj_code'] + '".', '2. Chọn trong gợi ý.'), '—',
         nl('- Gợi ý dạng "mã - tên".', '- ' + ('Chỉ nhà cung cấp đang hoạt động.' if ncc else 'Tìm theo tên, mã hoặc số điện thoại.'))),
        ('004', 'Cửa sổ chọn hợp đồng', 'P0', O + ' ' + c['obj_sample'] + '.',
         nl('1. Bấm "' + c['picker_btn'] + '".'), '—',
         nl('- Cửa sổ "' + c['picker_title'] + '".', '- Cột: ' + picker_cols + '.',
            ('- Ô lọc: Loại hợp đồng (14 lựa chọn), Số hợp đồng.' if not ncc else
             '- 2 tab: "HĐ Nhà cung cấp hiện tại", "HĐ Nhà cung cấp khác"; ô "Số hợp đồng..." và 2 nút tìm / làm mới; nút Đóng.'))),
        ('005', 'Bấm vào dòng hợp đồng để thêm', 'P0', 'Đang mở cửa sổ chọn hợp đồng.',
         nl('1. Bấm dòng hợp đồng ' + c['contract_sample'] + '.', '2. Bấm lại đúng dòng đó.', '3. Đóng cửa sổ.'), '—',
         nl('- Lần 1: thông báo xanh "Thêm thành công.", hợp đồng xuất hiện trong bảng.',
            '- Lần 2: thông báo vàng "Hợp đồng đã được chọn.", không thêm trùng.',
            '- Dòng mới: Loại dư mặc định "Dư nợ"' + (', Tài khoản lấy theo dòng phía trên, Loại tiền theo hợp đồng (VNĐ thì Tỷ giá = 1).' if ncc else '.'))),
    ]
    if not ncc:
        S3 += [
            ('006', 'Để trống Loại hợp đồng chỉ ra hợp đồng bán', 'P1', 'Khách hàng có hợp đồng bán, hợp đồng hãng, hợp đồng đầu kỳ.',
             nl('1. Mở cửa sổ chọn hợp đồng, không chọn Loại hợp đồng.', '2. Chọn Loại hợp đồng = Hợp đồng hãng.', '3. Chọn = Hợp đồng đầu kỳ.'), '—',
             nl('- Để trống: chỉ hợp đồng bán (Hợp đồng / Đơn hàng / Phụ lục…) Đã duyệt hoặc Có hiệu lực.',
                '- Hợp đồng hãng: chỉ hợp đồng hãng Có hiệu lực, loại Hợp đồng hoặc Hợp đồng dự án.',
                '- Hợp đồng đầu kỳ: chỉ hợp đồng đầu kỳ của khách hàng.',
                '- Lưu ý (hành vi hiện tại của ERP): Hợp đồng đầu kỳ và Hợp đồng dự án chỉ hiện hợp đồng do CHÍNH người đăng nhập tạo.')),
            ('007', 'Các loại hợp đồng mua trong cửa sổ khách hàng', 'P2', '—',
             nl('1. Lần lượt chọn Hợp đồng mua nước ngoài, Hợp đồng mua ngoài, Hợp đồng mua trong nước.'), '—',
             nl('- Lưu ý (hành vi hiện tại của ERP): "Hợp đồng mua nước ngoài" luôn trống; "Hợp đồng mua ngoài" '
                'hiện hợp đồng của mọi đối tượng, không lọc theo khách hàng đang chọn.')),
        ]
    else:
        S3 += [
            ('006', 'Tab HĐ Nhà cung cấp khác', 'P1', 'Nhà cung cấp FLY.',
             nl('1. Mở cửa sổ chọn hợp đồng.', '2. Bấm tab "HĐ Nhà cung cấp khác".', '3. Bấm 1 dòng.'), '—',
             nl('- Tab hiện hợp đồng của các nhà cung cấp KHÁC FLY.', '- Bấm dòng vẫn thêm được vào khai báo của FLY.')),
            ('007', 'Hợp đồng đã khai báo trước đó', 'P0', 'Hợp đồng H của FLY đã có khai báo đầu kỳ.',
             nl('1. Bấm dòng H trong tab "HĐ Nhà cung cấp hiện tại".'), '—',
             nl('- Thông báo vàng "Hợp đồng đã được chọn.", không thêm.')),
            ('008', 'Đổi tài khoản 1 dòng áp cho mọi dòng', 'P2', 'Bảng có 3 dòng.',
             nl('1. Đổi Tài khoản ở dòng 1 sang 3311.'), '—',
             nl('- Cả 3 dòng đều đổi sang tài khoản 3311.')),
            ('009', 'Loại tiền và Tỷ giá', 'P0', 'Dòng hợp đồng mua nước ngoài.',
             nl('1. Chọn Loại tiền VNĐ.', '2. Đổi sang USD, nhập Tỷ giá 25,450.'), '—',
             nl('- VNĐ: Tỷ giá = 1 và ô bị khoá.', '- USD: nhập được tỷ giá.')),
            ('010', 'Đổi nhà cung cấp khi đã chọn hợp đồng', 'P2', 'Bảng có 2 dòng.',
             nl('1. Đổi ô Nhà cung cấp sang nhà cung cấp khác.'), '—',
             nl('- Bảng hợp đồng bị xoá trống.')),
        ]
    n = len(S3)
    S3 += [
        ('%03d' % (n + 1), 'Lưu thành công', 'P0', 'Đã chọn 2 hợp đồng của ' + c['obj_sample'] + '.',
         nl('1. Dòng 1: Tài khoản ' + c['account_no'] + ', Dư nợ, Công nợ 1,500,000' + (', Loại tiền USD, Tỷ giá 25,450' if ncc else '') + '.',
            '2. Dòng 2: Tài khoản ' + c['account_no'] + ', bấm nút Dư nợ đổi thành Dư có, Công nợ 500,000.', '3. Bấm Lưu.'), '—',
         nl('- Thông báo xanh "' + c['msg_add'] + '", cửa sổ đóng, lưới tải lại.',
            '- Có 2 khai báo mới, mã dạng ' + c['code_rule'] + '.',
            '- Sổ chi tiết công nợ có 2 bút toán tương ứng, ngày 01/08/2025' + (', bút toán USD quy đổi = 1,500,000 × 25,450.' if ncc else '.'))),
        ('%03d' % (n + 2), 'Lưu khi chưa nhập Tài khoản / Công nợ', 'P0', 'Đã chọn 1 hợp đồng, chưa nhập gì.',
         nl('1. Bấm Lưu.'), '—',
         nl('- Dưới ô Tài khoản báo "Bắt buộc chọn một tài khoản".', '- Dưới ô Công nợ báo "Bắt buộc phải nhập".', '- Cửa sổ không đóng.')),
        ('%03d' % (n + 3), 'Lưu khi chưa chọn hợp đồng nào', 'P1', 'Đã chọn ' + o + ', bảng trống.',
         nl('1. Bấm Lưu.'), '—', nl('- Báo lỗi "Phải chọn ít nhất một hợp đồng".')),
        ('%03d' % (n + 4), 'Công nợ nhỏ hơn 1', 'P1', '—', nl('1. Nhập Công nợ 0, Lưu.'), '—',
         nl('- Dưới ô Công nợ báo "Giá trị không hợp lệ".')),
        ('%03d' % (n + 5), 'Trùng khai báo đã có', 'P0', 'Hợp đồng H + tài khoản ' + c['account_no'] + ' đã khai báo cho ' + o + ' X' +
         ('' if ncc else ' (chọn lại được H vì cửa sổ không chặn)') + '.',
         nl('1. Lập khai báo X + H + ' + c['account_no'] + '.', '2. Bấm Lưu.'), '—',
         nl('- Dưới ô Tài khoản báo "Đã khai báo đầu kỳ cho tài khoản này".', '- Không dòng nào được lưu trong lần bấm đó.')),
        ('%03d' % (n + 6), 'Bấm Hủy', 'P2', 'Đã nhập dở.', nl('1. Bấm Hủy.'), '—', nl('- Cửa sổ đóng, không lưu, không hỏi xác nhận.')),
        ('%03d' % (n + 7), 'Xoá dòng trên cửa sổ Thêm mới', 'P2', 'Bảng có 2 dòng.', nl('1. Bấm dấu x đỏ cuối dòng 1.'), '—',
         nl('- Dòng 1 bị bỏ khỏi bảng.')),
    ]

    S4 = [
        ('001', 'Mở cửa sổ Sửa', 'P0', 'Khai báo Z (' + ('mọi khai báo' if not ncc else 'chưa có chứng từ khác') + ').',
         nl('1. Bấm nút bút chì ở dòng Z.'), '—',
         nl('- Cửa sổ "' + c['modal_edit'] + '" điền sẵn dữ liệu.', '- Ô ' + c['form_obj_label'] + ' bị khoá; không có nút chọn hợp đồng, không có dấu x xoá dòng.',
            '- Sửa được: Tài khoản, Dư nợ / Dư có, Công nợ' + (', Loại tiền, Tỷ giá.' if ncc else '.'))),
        ('002', 'Lưu thay đổi', 'P0', 'Đang sửa Z.',
         nl('1. Đổi sang Dư có, Công nợ 2,750,000.', '2. Bấm Lưu.'), '—',
         nl('- Thông báo "' + c['msg_edit'] + '", lưới tải lại, Z hiện ở cột Dư có.', '- Bút toán trong sổ đổi theo.')),
        ('003', 'Đổi tài khoản khi sửa', 'P2', 'Z dùng tài khoản ' + c['account_no'] + '.',
         nl('1. Đổi sang tài khoản khác, Lưu.'), '—',
         nl('- Lưu thành công.',
            '- Lưu ý (hành vi hiện tại của ERP): không kiểm trùng với khai báo khác cùng hợp đồng; trong sổ, cột số tài khoản của bút toán vẫn ghi số cũ.')),
    ]
    if not ncc:
        S4.append(('004', 'Sửa khai báo đã có phiếu thu', 'P1', 'Khai báo Y đã có phiếu thu / phiếu kế toán cho hợp đồng.',
                   nl('1. Bấm Sửa ở dòng Y.'), '—',
                   nl('- Lưu ý (hành vi hiện tại của ERP): vẫn mở và lưu được — màn khách hàng không chặn khai báo đã phát sinh chứng từ.')))
    else:
        S4.append(('004', 'Khai báo đã có chứng từ khác', 'P0', 'Hợp đồng + tài khoản của Y đã có phiếu chi / phiếu kế toán / phiếu nhập ghi sổ.',
                   nl('1. Tìm dòng Y.'), '—', nl('- Dòng Y không có nút Sửa và Xóa.')))

    S5 = [
        ('001', 'Xóa khai báo', 'P0', 'Khai báo Z có nút Xóa.',
         nl('1. Bấm dấu x đỏ ở dòng Z.', '2. Bấm Hủy.', '3. Bấm lại, bấm Xác nhận.'), '—',
         nl('- Hộp "Xác nhận xóa!" với câu "Bạn chắc chắn muốn xóa bản ghi này?", 2 nút Xác nhận / Hủy.',
            '- Hủy: không đổi gì.', '- Xác nhận: trang tải lại, thông báo "' + c['msg_del'] + '", Z biến mất.',
            '- Bút toán của Z trong sổ chi tiết công nợ cũng mất.')),
    ]
    if not ncc:
        S5.append(('002', 'Xóa khai báo đã có phiếu thu', 'P1', 'Khai báo Y đã có phiếu thu gắn vào.',
                   nl('1. Xóa Y.'), '—',
                   nl('- Lưu ý (hành vi hiện tại của ERP): xoá được; báo cáo công nợ của hợp đồng sẽ lệch vì phiếu thu còn mà số dư đầu kỳ mất.')))

    imp_cols = ('STT, Mã Khách Hàng (*), Mã hợp đồng (*), Loại hợp đồng, Số Tài khoản (*), Loại dư, Công nợ (*)' if not ncc else
                'STT, Nhà cung cấp (*), Mã hợp đồng mua (*), Loại hợp đồng mua, Số Tài khoản (*), Loại tiền (*), Tỷ giá, Loại dư, Công nợ (*)')
    codes = ('HDMNN, HDMN, HDMTN (hợp đồng mua), HDDK (đầu kỳ), HDHNTDA (hãng / dự án), HDDV (dịch vụ BH-SC)' if not ncc else
             'HDMNN (mua nước ngoài), HDMN (mua ngoài), HDMTN (mua trong nước), HDMDK (mua đầu kỳ)')
    S6 = [
        ('001', 'Mở cửa sổ Import và tải file mẫu', 'P1', '—',
         nl('1. Bấm "Import excel".', '2. Bấm "(File mẫu)".'), '—',
         nl('- Cửa sổ "Import Excel" có ô "Chọn file (*)", liên kết "(File mẫu)", nút Import, Hủy.',
            '- Tải về ' + c['sample_file'] + ' với các cột: ' + imp_cols + '.')),
        ('002', 'Import file hợp lệ', 'P0', 'File 2 dòng hợp lệ, mã loại hợp đồng dùng: ' + codes + '.',
         nl('1. Chọn file.', '2. Bấm Import.'), '—',
         nl('- Thông báo xanh, cửa sổ đóng, lưới có 2 khai báo mới và có bút toán trong sổ.',
            '- Lưu ý (hành vi hiện tại của ERP): câu thông báo chỉ ghi "Thao tác thành công", không ghi số bản ghi.')),
        ('003', 'File có dòng lỗi', 'P0', 'File 3 dòng: 1 đúng, 1 thiếu ' + o + ', 1 sai tài khoản và loại dư.',
         nl('1. Import.', '2. Bấm dòng "Không hợp lệ: ... bản ghi" để xem chi tiết.'), '—',
         nl('- Thông báo "Import thất bại!"; trong cửa sổ hiện "Không hợp lệ: 2 bản ghi".',
            '- Chi tiết dạng "- Dòng <số dòng excel>: <lỗi>", ví dụ: "' +
            ('Thiếu thông tin bắt buộc (Khách hàng, Hợp đồng, Tài khoản, Công nợ)' if not ncc else
             'Thiếu thông tin bắt buộc (Nhà cung cấp, Hợp đồng, Loại Hợp đồng, Tài khoản, Loại tiền, Công nợ)') +
            '", "Tài khoản không tồn tại trong hệ thống", "Loại dư phải là \"Dư nợ\" hoặc \"Dư có\"".',
            '- KHÔNG dòng nào được lưu, kể cả dòng đúng.')),
        ('004', 'Các câu lỗi khác của import', 'P1', '—',
         nl('1. Lần lượt import: mã ' + o + ' không có thật; công nợ âm; hợp đồng đã khai báo' + ('; loại tiền sai; tỷ giá 0' if ncc else '') + '.'), '—',
         nl('- "' + ('Mã khách hàng không tồn tại trong hệ thống' if not ncc else 'Mã nhà cung cấp không tồn tại trong hệ thống') + '".',
            '- "Công nợ phải là số dương".', '- "Hợp đồng đã được khai báo công nợ đầu kỳ".'
            + ('\n- "Loại tiền không tồn tại trong hệ thống"; "Tỷ giá phải là số dương".' if ncc else ''))),
        ('005', 'Mã hợp đồng không có thật', 'P1', 'File có dòng mã hợp đồng gõ sai.',
         nl('1. Import.'), '—',
         nl(('- Lưu ý (hành vi hiện tại của ERP): màn khách hàng không báo lỗi gọn mà hiện trang lỗi hệ thống (không có câu thông báo).'
             if not ncc else '- Báo "Hợp đồng mua không tồn tại trong hệ thống".'),
            ('- Lưu ý: import khách hàng không kiểm hợp đồng có thuộc khách hàng trong file hay không.' if not ncc else
             '- Lưu ý: không kiểm hợp đồng có thuộc nhà cung cấp trong file hay không.'))),
    ]

    S7 = [
        ('001', 'In danh sách', 'P0', 'Đang lọc theo ' + o + ' ' + c['obj_code'] + '.',
         nl('1. Bấm "In".'), '—',
         nl('- Mở trang in khổ NGANG có logo công ty và bảng: STT, ' + c['code_col'] + ', Tài khoản, ' + O +
            ', Loại hợp đồng, Mã hợp đồng, Dư nợ, Dư có, Người tạo, Ngày tạo, Người sửa, Ngày sửa.',
            '- Chỉ in các dòng khớp bộ lọc.' + ('\n- Lưu ý: bản in nhà cung cấp không có cột Loại tiền, Tỷ giá; số tiền là nguyên tệ.' if ncc else ''))),
        ('002', 'Xuất excel', 'P0', 'Đang lọc theo ' + o + ' ' + c['obj_code'] + '.',
         nl('1. Bấm "Xuất excel".'), '—',
         nl('- Tải file ' + c['file_export'] + ' ngay (không hỏi chọn cột).', '- Đầu file có logo và tiêu đề "' + c['export_title'] + '".',
            '- Cùng 12 cột như bản in; cuối file có "Ngày ..., tháng ..., năm ..." và "Người lập (Ký, họ tên)".')),
    ]

    S8 = [
        ('001', 'Luồng chính: khai báo rồi kiểm sổ', 'P0', O + ' ' + c['obj_sample'] + ' có hợp đồng ' + c['contract_sample'] + ' chưa khai báo.',
         nl('1. Tạo mới khai báo ' + ('Dư nợ 1,500,000' if not ncc else 'Dư có 1,000 USD tỷ giá 25,450') + ', tài khoản ' + c['account_no'] + '.',
            '2. Mở báo cáo Sổ chi tiết công nợ ' + ('phải thu khách hàng' if not ncc else 'phải trả nhà cung cấp') + ' của ' + o + ' đó.',
            '3. Sửa khai báo, xem lại sổ.', '4. Xóa khai báo, xem lại sổ.'), '—',
         nl('- Bước 2: có bút toán ngày 01/08/2025, chứng từ là mã khai báo, số tiền ' + ('1,500,000 bên Nợ' if not ncc else '1,000 USD, quy đổi 25,450,000 bên Có') + '.',
            '- Bước 3: số tiền trên sổ đổi theo.', '- Bước 4: bút toán biến mất.')),
        ('002', 'Hai người lập cùng hợp đồng', 'P2', '2 tài khoản mở cửa sổ Thêm mới cùng lúc, cùng ' + o + ' + hợp đồng + tài khoản.',
         nl('1. Người 1 Lưu.', '2. Người 2 Lưu.'), '—',
         nl('- Người 1 thành công.', '- Người 2 nhận "Đã khai báo đầu kỳ cho tài khoản này".')),
    ]

    return [
        ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
        ('II', 'BỘ LỌC & TÌM KIẾM', S2),
        ('III', 'THÊM MỚI', S3),
        ('IV', 'SỬA', S4),
        ('V', 'XÓA', S5),
        ('VI', 'IMPORT EXCEL', S6),
        ('VII', 'IN & XUẤT EXCEL', S7),
        ('VIII', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S8),
    ]


for cfg in (KH, NCC):
    print('=' * 20, cfg['out'])
    build(output_file=os.path.join(BASE, cfg['out']),
          sheet_name='Trang tính1',
          feature_name=cfg['title'] + ' (ERP)',
          module_name=cfg['module'],
          description_block=description(cfg),
          role_tcs=role_tcs(cfg),
          sections=sections(cfg))
