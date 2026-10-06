# -*- coding: utf-8 -*-
"""Sinh 2 file testcase cho 2 man Khai bao dau ky cong no (phan he Tai chinh):

  - "testcase - Khai bao dau ky cong no.xlsx"            (khach hang)
  - "testcase - Khai bao dau ky cong no nha cung cap.xlsx" (nha cung cap)

Muc dich (user yeu cau 02/10/2026): gui tester HIEU LUONG ERP va TEST BEN HRM. Moi testcase mo ta
hanh vi tren HRM; cho nao HRM KHAC ERP (sua loi ERP / doi cach lam) thi ghi them 1 gach dau dong
"Đối chiếu ERP: ..." trong cot Ket qua mong doi — tester mo 2 cong song song de doi chieu.

Viet tu code HRM nhanh develop + khao sat ERP TanPhatDev ngay 01-02/10/2026. So lieu tien dieu kien
lay tu DB local gop_db (cong ty TPE). Ngon ngu NGHIEP VU cho QA — khong dung thuat ngu code.
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


# =====================================================================================================
# Cau hinh 2 man
# =====================================================================================================
KH = dict(
    key='kh',
    title='Khai báo đầu kỳ công nợ',
    module='Khai báo đầu kỳ công nợ KH',
    obj='khách hàng', Obj='Khách hàng',
    menu='Tài chính > nhóm Khai báo đầu kỳ > Khai báo đầu kỳ công nợ',
    menu2='Tài chính > Kế toán công nợ > nhóm Khách hàng > Công nợ đầu kỳ theo khách hàng - hợp đồng',
    erp_menu='Kế toán > Khai báo đầu kỳ > Khai báo đầu kỳ công nợ (và Kế toán > Kế toán công nợ > '
             'Khách hàng > Công nợ đầu kỳ theo khách hàng - hợp đồng)',
    code_sample='TPE.CNĐKHĐ.03364', code_rule='<mã công ty>.CNĐKHĐ.<số thứ tự 5 chữ số>',
    account='1311 - Phải thu của khách hàng ngắn hạn', account_no='1311',
    obj_sample='75TPHXCH-2 - CÔNG TY CỔ PHẦN KIM LONG MOTORS HUẾ', obj_code='75TPHXCH-2',
    contract_sample='HĐ_TPE_HN_KD3_26_0548_HD2605-0004', contract_type='Hợp đồng hãng',
    total_company=1134, total_all=1746, used=1519,
    perm_manage='Quản lý công nợ đầu kỳ',
    perm_create='Quản lý công nợ đầu kỳ', perm_edit='Quản lý công nợ đầu kỳ', perm_delete='Quản lý công nợ đầu kỳ',
    has_currency=False,
    file='testcase HRM - Khai bao dau ky cong no.xlsx',
    print_title='Công nợ đầu kỳ theo khách hàng - hợp đồng',
)
NCC = dict(
    key='ncc',
    title='Khai báo đầu kỳ công nợ nhà cung cấp',
    module='Khai báo đầu kỳ công nợ NCC',
    obj='nhà cung cấp', Obj='Nhà cung cấp',
    menu='Tài chính > nhóm Khai báo đầu kỳ > Khai báo đầu kỳ công nợ nhà cung cấp',
    menu2=None,
    erp_menu='Kế toán > Khai báo đầu kỳ > Khai báo đầu kỳ công nợ nhà cung cấp',
    code_sample='TPE_DKNCC_01308', code_rule='<mã công ty>_DKNCC_<số thứ tự 5 chữ số>',
    account='3311 - Phải trả cho người bán ngắn hạn', account_no='3311',
    obj_sample='FLY - ZHONGSHAN EAGLE-FLY ELECTRICAL APPLIANCE CO.,LTD', obj_code='FLY',
    contract_sample='FLY 0726 HP-ANNEX 01', contract_type='Hợp đồng mua nước ngoài',
    total_company=1141, total_all=1141, used=497,
    perm_manage=None,
    perm_create='Khai báo thêm công nợ đầu kỳ nhà cung cấp',
    perm_edit='Khai báo sửa công nợ đầu kỳ nhà cung cấp',
    perm_delete='Khai báo xoá công nợ đầu kỳ nhà cung cấp',
    has_currency=True,
    file='testcase HRM - Khai bao dau ky cong no nha cung cap.xlsx',
    print_title='Danh sách khai báo công nợ đầu kỳ nhà cung cấp',
)

SCOPE_PERMS = [
    'Xem tất cả công nợ đầu kỳ',
    'Xem tất cả công nợ đầu kỳ của công ty',
    'Xem tất cả công nợ đầu kỳ của phòng ban',
    'Xem tất cả công nợ đầu kỳ của bộ phận',
]


def nl(*lines):
    return '\n'.join(lines)


# =====================================================================================================
# Khoi mo ta 9 muc
# =====================================================================================================
def description(c):
    is_ncc = c['has_currency']
    purpose = nl(
        'Màn hình "{t}" khai báo SỐ DƯ CÔNG NỢ ĐẦU KỲ của từng hợp đồng × từng tài khoản cho một {o}, '
        'làm số mở đầu cho sổ chi tiết công nợ và các báo cáo công nợ.'.format(t=c['title'], o=c['obj']),
        'Mỗi dòng khai báo ghi đúng MỘT bút toán vào sổ chi tiết tài khoản (Nợ hoặc Có tài khoản '
        '{a}), ngày hạch toán = "Ngày tính công nợ" cấu hình chung (hiện là 01/08/2025).'.format(a=c['account_no']),
        'Luồng: chọn {o}, rồi bấm "Chọn hợp đồng" chọn một hoặc nhiều hợp đồng, rồi mỗi dòng nhập Tài khoản, '
        'Loại dư (Dư nợ / Dư có), Công nợ{cur}, cuối cùng bấm Lưu. Mỗi dòng thành một phiếu khai báo riêng có mã '
        'dạng {rule}.'.format(o=c['obj'], rule=c['code_rule'],
                              cur=', Loại tiền, Tỷ giá' if is_ncc else ''),
        'Màn này đã chuyển từ hệ thống cũ (ERP) sang hệ thống mới (HRM). Hai bên dùng CHUNG dữ liệu: '
        'khai báo lập bên HRM hiện ngay trong báo cáo công nợ bên ERP và ngược lại.',
        'Đường dẫn HRM: ' + c['menu'] + ('\nLối vào thứ hai (giống ERP): ' + c['menu2'] if c['menu2'] else ''),
        'Đường dẫn ERP để đối chiếu: ' + c['erp_menu'] + '.',
        'Cách đọc file: mỗi testcase mô tả kết quả trên HRM; chỗ nào HRM KHÁC ERP có thêm dòng '
        '"Đối chiếu ERP: ..." để tester mở 2 hệ thống song song so sánh.')

    shown = nl(
        'Danh sách hiển thị khai báo theo PHẠM VI QUYỀN XEM (dùng chung cho cả 2 màn khách hàng và nhà '
        'cung cấp), xét lần lượt, gặp quyền nào trước thì dùng quyền đó:',
        '- "Xem tất cả công nợ đầu kỳ": mọi khai báo của mọi công ty.',
        '- "Xem tất cả công nợ đầu kỳ của công ty": khai báo thuộc công ty của người đăng nhập.',
        '- "Xem tất cả công nợ đầu kỳ của phòng ban": khai báo thuộc các phòng ban người đăng nhập '
        'được giao quản lý.',
        '- "Xem tất cả công nợ đầu kỳ của bộ phận": khai báo thuộc các bộ phận được giao quản lý.',
        '- Không có quyền nào ở trên: chỉ khai báo do chính mình tạo.',
        'Công ty / phòng ban / bộ phận của một khai báo = của NGƯỜI LẬP HỢP ĐỒNG (không phải người lập '
        'khai báo).',
        'Cửa sổ "Chọn hợp đồng" ' + (
            'hiện đủ 8 nguồn như ERP: Hợp đồng bán (Hợp đồng / Đơn hàng / HĐ nguyên tắc / HĐ thúc đẩy '
            'bán / ĐH thúc đẩy bán / Phụ lục bổ sung / Phụ lục HĐNT — chỉ hợp đồng Đã duyệt hoặc Có '
            'hiệu lực), Hợp đồng hãng (Có hiệu lực, loại Hợp đồng hoặc Hợp đồng dự án), Hợp đồng gói '
            'dịch vụ, Hợp đồng dự án (khác Đang tạo), Hợp đồng đầu kỳ, Hợp đồng mua nước ngoài, Hợp '
            'đồng mua ngoài, Hợp đồng mua trong nước — luôn chỉ hợp đồng CỦA khách hàng đang chọn.'
            if not is_ncc else
            'gộp 4 nguồn hợp đồng mua như ERP: Hợp đồng mua nước ngoài, Hợp đồng mua ngoài, Hợp đồng '
            'mua trong nước, Hợp đồng mua đầu kỳ — mọi trạng thái. Ô "Phạm vi" chọn hợp đồng của nhà '
            'cung cấp đang chọn hoặc của nhà cung cấp KHÁC (2 tab của ERP).'),
        'Danh sách tài khoản: ' + (
            'mọi tài khoản CHI TIẾT (tài khoản lá) đang hoạt động — giữ như ERP.' if not is_ncc else
            'tài khoản chi tiết đang hoạt động có đánh dấu "Theo dõi công nợ" — giữ như ERP.'))

    hidden = nl(
        '- Khai báo ngoài phạm vi quyền xem: không hiện ở danh sách, mở bằng đường dẫn trực tiếp thì '
        'chuyển sang trang "Không tìm thấy".',
        '- Trong cửa sổ "Chọn hợp đồng": hợp đồng ĐÃ khai báo cho {o} này vẫn hiện nhưng mờ, cột Tình '
        'trạng ghi "Đã khai báo", bấm không thêm được; hợp đồng đã có trên form ghi "Đã chọn".'.format(o=c['obj']),
        '- Nút Sửa / Xóa ẨN HẲN (không hiện xám) khi khai báo ĐÃ PHÁT SINH CHỨNG TỪ CÔNG NỢ: cùng hợp '
        'đồng + tài khoản + {o} đã có phiếu thu, phiếu chi, phiếu báo có, ủy nhiệm chi hoặc phiếu kế '
        'toán ghi sổ. Dữ liệu thật hiện có {u} khai báo thuộc diện này.'.format(o=c['obj'], u=c['used']),
        '- Phiếu xuất hàng / nhập hàng / hạch toán dịch vụ trên cùng hợp đồng KHÔNG tính là "đã phát '
        'sinh" (đó là phát sinh trong kỳ, không trừ vào số dư đầu kỳ).',
        '- Tài khoản đang khoá: không có trong danh sách chọn mới; khai báo cũ đang dùng tài khoản khoá '
        'vẫn hiện đúng tên kèm biểu tượng khoá.' + (
            '\n- Loại tiền đang khoá: tương tự tài khoản. Riêng VNĐ luôn chọn được.' if is_ncc else ''))

    time_filter = nl(
        'Ô lọc "Ngày tạo" (một ô chọn khoảng từ – đến) lọc theo NGÀY LẬP khai báo, lấy trọn 2 đầu mút.',
        '"Ngày tính công nợ" KHÔNG phải ô lọc: đây là ngày hạch toán cố định lấy từ cấu hình chung '
        '(01/08/2025), mọi khai báo cùng một giá trị.')

    structure = nl(
        'Một lần lập = một {o} × nhiều hợp đồng; mỗi dòng hợp đồng lưu thành MỘT khai báo riêng (một mã '
        'phiếu riêng, một bút toán riêng).'.format(o=c['obj']),
        'Khai báo gồm: Mã phiếu, {O}, Loại hợp đồng, Số hợp đồng, Tài khoản, Loại dư, Công nợ{cur}, '
        'Ngày tính công nợ, Người tạo / Ngày tạo, Người cập nhật / Ngày cập nhật.'.format(
            O=c['Obj'], cur=', Loại tiền, Tỷ giá, Quy đổi (VND), Người lập hợp đồng' if is_ncc else ''),
        'Màn Sửa và Chi tiết chỉ có ĐÚNG MỘT dòng; {o} và hợp đồng bị khoá, không đổi được.'.format(o=c['obj']))

    rules = nl(
        '- Không được trùng: cùng {o} + cùng hợp đồng + cùng tài khoản chỉ khai báo một lần (kể cả trên '
        'cùng một form và kể cả khi Sửa đổi sang tài khoản đã có).'.format(o=c['obj']),
        '- Công nợ phải lớn hơn 0. Dư nợ ghi Nợ tài khoản, Dư có ghi Có tài khoản.',
        ('- Hợp đồng phải THUỘC khách hàng đang chọn (ERP cũ không kiểm khi import).' if not is_ncc else
         '- Hợp đồng được chọn của nhà cung cấp khác (giữ như ERP).'),
        ('- Quy đổi (VND) = Công nợ × Tỷ giá, làm tròn đến đồng. Loại tiền VNĐ thì Tỷ giá luôn là 1 và '
         'ô Tỷ giá bị khoá. Khác VNĐ thì Tỷ giá bắt buộc, lớn hơn 0.' if is_ncc else
         '- Khai báo khách hàng luôn là VNĐ, tỷ giá 1.'),
        '- Sửa / Xóa khai báo thì bút toán trong sổ được sửa / xoá theo ngay.')

    perms = nl(
        'Quyền thao tác:',
        ('- "Quản lý công nợ đầu kỳ": vào màn, xem, thêm, sửa, xoá, import (giữ như ERP — một quyền '
         'cho cả màn).' if not is_ncc else
         '- Xem màn: KHÔNG cần quyền riêng (giữ như ERP), dữ liệu theo phạm vi xem bên dưới.\n'
         '- "Khai báo thêm công nợ đầu kỳ nhà cung cấp": nút Tạo mới, Import Excel, cửa sổ chọn hợp đồng.\n'
         '- "Khai báo sửa công nợ đầu kỳ nhà cung cấp": nút Sửa.\n'
         '- "Khai báo xoá công nợ đầu kỳ nhà cung cấp": nút Xóa.'),
        'Quyền phạm vi xem (dùng chung 2 màn): ' + '; '.join('"%s"' % p for p in SCOPE_PERMS) + '.',
        'Lưu ý: quyền phải được cấp ở màn Phân quyền của HRM (nhóm "Khai báo đầu kỳ công nợ"'
        + (' / "Khai báo đầu kỳ công nợ nhà cung cấp"' if is_ncc else '') + '). '
        'Người chỉ có quyền ở ERP sẽ không thấy mục menu bên HRM.',
        'Đối chiếu ERP: ' + ('ERP chặn cả màn bằng "Quản lý công nợ đầu kỳ" — HRM giữ nguyên.' if not is_ncc else
                             'ERP chỉ ẨN nút theo 3 quyền, gọi thẳng chức năng vẫn làm được; HRM chặn thật.'))

    stats = nl(
        'Ô "Hiển thị a–b / N" dưới bảng: a, b là dòng đầu / cuối của trang, N là tổng khai báo khớp bộ '
        'lọc và phạm vi quyền.',
        'Cột "Dư nợ" chỉ có số khi Loại dư = Dư nợ; cột "Dư có" chỉ có số khi Loại dư = Dư có; cột còn '
        'lại để TRỐNG (không ghi 0, không ghi dấu gạch).' + (
            '\nCột "Quy đổi (VND)" = Công nợ × Tỷ giá, làm tròn đến đồng.' if is_ncc else ''))

    notes = nl(
        '- Số hiển thị theo chuẩn quốc tế: dấu phẩy ngăn hàng nghìn, dấu chấm phần thập phân '
        '(1,500,000 · 2,750,000.5).',
        '- Bản in danh sách tối đa 2,000 dòng; vượt thì báo phải thu hẹp bộ lọc, không in một phần.',
        '- Khai báo không có tên riêng nên tiêu đề cửa sổ Lịch sử dùng MÃ PHIẾU.',
        '- Khách hàng / nhà cung cấp trên máy phát triển có thể thiếu so với thật nên ô ' + c['Obj'] +
        ' trống ở một số dòng cũ là do dữ liệu, không phải lỗi màn.',
        '- Kiểm sổ: sau mỗi lần Lưu / Sửa / Xóa nên mở báo cáo "Sổ chi tiết công nợ ' +
        ('phải thu khách hàng' if not is_ncc else 'phải trả nhà cung cấp') +
        '" bên ERP để thấy bút toán tương ứng xuất hiện / đổi / mất.',
        '- Nhóm testcase gọi thẳng chức năng bỏ qua giao diện dành cho tester kỹ thuật.')

    return [
        ('1. Mục đích tính năng', purpose),
        ('2. Đối tượng được tính / hiển thị', shown),
        ('3. Đối tượng bị ẩn / không tính', hidden),
        ('4. Bộ lọc thời gian áp dụng cho', time_filter),
        ('5. Cấu trúc dữ liệu / cây phân cấp', structure),
        ('6. Quy tắc cộng dồn / deduplicate', rules),
        ('7. Phân quyền cấp', perms),
        ('8. Cách tính các ô thống kê', stats),
        ('9. Ghi chú đọc bảng', notes),
    ]


# =====================================================================================================
# Phan quyen
# =====================================================================================================
def role_tcs(c):
    menu = c['menu']
    tcs = []
    if c['perm_manage']:
        tcs += [
            ('00', 'Không có quyền "Quản lý công nợ đầu kỳ" thì không thấy màn', 'P0',
             'Tài khoản A KHÔNG có quyền "Quản lý công nợ đầu kỳ" ở HRM.',
             nl('1. Đăng nhập bằng A.', '2. Mở phân hệ Tài chính, nhóm Khai báo đầu kỳ.',
                '3. Dán đường dẫn màn danh sách lên thanh địa chỉ.'),
             '—',
             nl('- Menu KHÔNG có mục "Khai báo đầu kỳ công nợ", nhóm Kế toán công nợ > Khách hàng cũng '
                'không có "Công nợ đầu kỳ theo khách hàng - hợp đồng".',
                '- Dán đường dẫn: chuyển sang trang "Không tìm thấy hoặc không được cấp quyền truy cập".',
                '- Đối chiếu ERP: ERP cũng chặn cả màn bằng đúng quyền này.')),
            ('01', 'Quyền "Quản lý công nợ đầu kỳ" dùng được toàn bộ chức năng', 'P0',
             nl('Tài khoản B có "Quản lý công nợ đầu kỳ" + "Xem tất cả công nợ đầu kỳ của công ty".',
                'Công ty của B (TPE) có {n} khai báo.'.format(n=c['total_company'])),
             nl('1. Đăng nhập bằng B.', '2. Vào ' + menu + '.'),
             '—',
             nl('- Danh sách hiện, ô thống kê ghi "Hiển thị 1–10 / {n}".'.format(n=c['total_company']),
                '- Có đủ nút Tạo mới, Import Excel, Xuất Excel, In danh sách, Cấu hình cột hiển thị.',
                '- Khai báo chưa phát sinh chứng từ có nút Sửa, Xóa; mọi dòng có Lịch sử.')),
        ]
    else:
        tcs += [
            ('00', 'Không có quyền nào vẫn vào được màn, chỉ thấy khai báo mình tạo', 'P0',
             nl('Tài khoản A không có quyền nào của nhóm khai báo đầu kỳ.',
                'A đã tạo 2 khai báo nhà cung cấp; công ty có 1,141 khai báo.'),
             nl('1. Đăng nhập bằng A.', '2. Vào ' + menu + '.'),
             '—',
             nl('- Màn mở được, chỉ hiện đúng 2 khai báo của A.',
                '- KHÔNG có nút Tạo mới, Import Excel; dòng KHÔNG có nút Sửa, Xóa.',
                '- Vẫn có Xuất Excel, In danh sách, Lịch sử.',
                '- Đối chiếu ERP: giống ERP (ERP không chặn quyền xem màn này).')),
            ('01', 'Quyền "Khai báo thêm công nợ đầu kỳ nhà cung cấp"', 'P0',
             'Tài khoản B chỉ có quyền thêm.',
             nl('1. Đăng nhập bằng B, vào ' + menu + '.', '2. Bấm Tạo mới, chọn nhà cung cấp, bấm "Chọn hợp đồng".'),
             '—',
             nl('- Có nút Tạo mới, Import Excel; mở được cửa sổ chọn hợp đồng, lưu được.',
                '- Dòng trên danh sách KHÔNG có nút Sửa, Xóa.')),
            ('02', 'Quyền "Khai báo sửa công nợ đầu kỳ nhà cung cấp"', 'P0',
             'Tài khoản C chỉ có quyền sửa; có khai báo X chưa phát sinh chứng từ.',
             nl('1. Đăng nhập bằng C, vào ' + menu + '.', '2. Quan sát dòng X, bấm Sửa.'),
             '—',
             nl('- Dòng X có nút Sửa, KHÔNG có nút Xóa.', '- Không có nút Tạo mới, Import Excel.',
                '- Màn Sửa mở được và lưu được.')),
            ('03', 'Quyền "Khai báo xoá công nợ đầu kỳ nhà cung cấp"', 'P0',
             'Tài khoản D chỉ có quyền xoá; có khai báo X chưa phát sinh chứng từ.',
             nl('1. Đăng nhập bằng D, vào ' + menu + '.', '2. Quan sát dòng X.'),
             '—',
             nl('- Dòng X có nút Xóa, KHÔNG có nút Sửa.',
                '- Đối chiếu ERP: ERP cũng ẩn/hiện theo 3 quyền này nhưng KHÔNG chặn khi gọi thẳng — xem TC "Gọi thẳng chức năng Thêm / Sửa / Xóa" cuối nhóm phân quyền.')),
        ]
    base = len(tcs)
    for i, p in enumerate(SCOPE_PERMS):
        expect = {
            0: 'Thấy khai báo của MỌI công ty; khối lọc có ô Công ty, Phòng ban, Bộ phận.',
            1: 'Chỉ thấy khai báo của công ty mình; khối lọc có ô Phòng ban, Bộ phận (không có ô Công ty).',
            2: 'Chỉ thấy khai báo thuộc các phòng ban được giao quản lý.',
            3: 'Chỉ thấy khai báo thuộc các bộ phận được giao quản lý.',
        }[i]
        tcs.append(('%02d' % (base + i), 'Phạm vi xem: "%s"' % p, 'P0' if i < 2 else 'P1',
                    nl('Tài khoản E%d chỉ có quyền "%s"%s.' % (i + 1, p,
                       ' và "Quản lý công nợ đầu kỳ"' if c['perm_manage'] else ''),
                       'Khai báo của khách hàng/nhà cung cấp do người lập hợp đồng thuộc công ty 1 / 4, '
                       'phòng ban HN_KD3, bộ phận P1.'),
                    nl('1. Đăng nhập bằng E%d.' % (i + 1), '2. Vào ' + c['menu'] + '.',
                       '3. Đếm tổng ở ô "Hiển thị a–b / N", mở bộ lọc nâng cao.'),
                    '—',
                    nl('- ' + expect,
                       '- Công ty / phòng ban / bộ phận tính theo NGƯỜI LẬP HỢP ĐỒNG.',
                       '- Đối chiếu ERP: cùng tài khoản, đếm bên ERP phải ra cùng N.')))
    nxt = len(tcs)
    tcs.append(('%02d' % nxt, 'Không có quyền phạm vi nào: chỉ thấy khai báo mình tạo', 'P0',
                nl('Tài khoản F%s không có quyền phạm vi nào.' % (' có "Quản lý công nợ đầu kỳ" nhưng' if c['perm_manage'] else ''),
                   'F tạo 3 khai báo.'),
                nl('1. Đăng nhập bằng F.', '2. Vào ' + c['menu'] + '.'),
                '—',
                nl('- Chỉ hiện 3 khai báo của F.', '- Khối lọc KHÔNG có ô Công ty / Phòng ban / Bộ phận.',
                   '- Mở đường dẫn chi tiết khai báo của người khác: trang "Không tìm thấy".')))
    nxt += 1
    tcs.append(('%02d' % nxt, 'Gọi thẳng chức năng Thêm / Sửa / Xóa khi không có quyền (tester kỹ thuật)', 'P0',
                'Tài khoản G không có quyền ' + ('"Quản lý công nợ đầu kỳ".' if c['perm_manage'] else 'thêm / sửa / xoá nhà cung cấp.'),
                nl('1. Dùng công cụ kiểm thử API, đăng nhập bằng G.',
                   '2. Gọi thẳng chức năng Thêm, Sửa, Xóa một khai báo, bỏ qua giao diện.'),
                '—',
                nl('- Cả 3 thao tác bị từ chối với câu "Bạn không có quyền thực hiện chức năng này.".',
                   '- Dữ liệu và sổ không đổi.',
                   '- Đối chiếu ERP: ' + ('ERP cũng chặn.' if c['perm_manage'] else
                                         'ERP KHÔNG chặn (chỉ ẩn nút) — HRM đã sửa.'))))
    nxt += 1
    tcs.append(('%02d' % nxt, 'Gọi thẳng Sửa / Xóa khai báo đã phát sinh chứng từ (tester kỹ thuật)', 'P0',
                'Khai báo Y đã có phiếu thu / phiếu kế toán ghi sổ cùng hợp đồng + tài khoản.',
                nl('1. Dùng công cụ kiểm thử API, đăng nhập bằng tài khoản có đủ quyền.',
                   '2. Gọi thẳng Sửa rồi Xóa khai báo Y.'),
                '—',
                nl('- Cả 2 bị từ chối với câu "Khai báo đã phát sinh chứng từ, không được sửa / xóa.".',
                   '- Đối chiếu ERP: ' + ('ERP màn khách hàng cho sửa / xoá thoải mái — HRM đã chặn.'
                                         if not c['has_currency'] else 'ERP chỉ ẩn nút, gọi thẳng vẫn làm được.'))))
    return tcs


# =====================================================================================================
# Cac section nghiep vu
# =====================================================================================================
def sections(c):
    is_ncc = c['has_currency']
    menu, O, o = c['menu'], c['Obj'], c['obj']
    acc = c['account']

    S1 = [
        ('001', 'Vào màn qua menu', 'P0',
         'Tài khoản B đủ quyền, phạm vi công ty; công ty TPE có {n} khai báo.'.format(n=c['total_company']),
         nl('1. Đăng nhập bằng B.', '2. Vào ' + menu + '.'),
         '—',
         nl('- Tiêu đề màn và tên tab trình duyệt là "{t}".'.format(t=c['title']),
            '- Bảng hiện 10 dòng, "Hiển thị 1–10 / {n}".'.format(n=c['total_company']),
            '- Khai báo mới lập nhất đứng đầu.')),
        ('002', 'Bộ cột mặc định', 'P0',
         'Tài khoản chưa từng tuỳ chỉnh cột ở màn này.',
         nl('1. Mở màn danh sách.', '2. Đọc tiêu đề cột từ trái sang phải.'),
         '—',
         nl('- Đúng thứ tự: STT, Mã phiếu, {O}, Số hợp đồng, {cur}Dư nợ, Dư có, Người tạo, Ngày tạo, '
            'Hành động.'.format(O=O, cur='Loại tiền, ' if is_ncc else ''),
            '- Các cột khác (Tài khoản, Loại hợp đồng, Ngày tính công nợ, Người cập nhật, Ngày cập nhật'
            + (', Người lập hợp đồng, Tỷ giá, Quy đổi (VND)' if is_ncc else '') +
            ') bật được ở "Cấu hình cột hiển thị".',
            '- Đối chiếu ERP: ERP hiện tất cả cột cùng lúc; HRM gọn hơn nhưng không thiếu cột nào.')),
        ('003', 'Mã phiếu là đường dẫn vào chi tiết', 'P1',
         'Có khai báo ' + c['code_sample'] + '.',
         nl('1. Bấm vào mã phiếu.', '2. Quay lại, bấm chuột phải vào mã phiếu.'),
         '—',
         nl('- Bấm trái mở màn Chi tiết, tiêu đề "Chi tiết {t}: {c}".'.format(t=c['title'].lower(), c=c['code_sample']),
            '- Chuột phải có "Mở liên kết trong tab mới".',
            '- Đối chiếu ERP: ' + ('ERP màn khách hàng KHÔNG có trang chi tiết (chỉ có popup Sửa).' if not is_ncc
                                  else 'ERP có trang chi tiết chỉ đọc; HRM thêm khối Lịch sử.'))),
        ('004', 'Số hợp đồng mở chứng từ gốc', 'P2',
         'Khai báo gắn hợp đồng hãng / hợp đồng đầu kỳ.',
         nl('1. Bấm vào số hợp đồng trên dòng.'),
         '—',
         nl('- Mở tab mới: hợp đồng có màn trên HRM thì mở HRM, chưa có thì mở trang hợp đồng bên ERP.',
            '- Hợp đồng mua chưa có trang để mở thì hiện chữ thường, không bấm được.')),
        ('005', 'Định dạng số, ngày, ô trống', 'P1',
         'Khai báo dư có 2,750,000.5; khai báo dư nợ 10,125,000.',
         nl('1. Tìm 2 khai báo trên.', '2. Đọc cột Dư nợ, Dư có, Ngày tạo.'),
         '—',
         nl('- Dư có hiện "2,750,000.5", cột Dư nợ cùng dòng để TRỐNG.',
            '- Dư nợ hiện "10,125,000", cột Dư có để trống.',
            '- Ngày tạo dạng dd/mm/yyyy HH:mm, không có giây.')),
    ]
    if c['menu2']:
        S1.append(('006', 'Lối vào thứ hai: Kế toán công nợ > Khách hàng', 'P0',
                   'Tài khoản B như TC_01.001.',
                   nl('1. Vào ' + c['menu2'] + '.', '2. So với danh sách mở từ nhóm Khai báo đầu kỳ.'),
                   '—',
                   nl('- Mở CÙNG màn "Khai báo đầu kỳ công nợ", cùng {n} khai báo.'.format(n=c['total_company']),
                      '- Đối chiếu ERP: ERP cũng đặt màn ở 2 chỗ này.')))

    S2 = [
        ('001', 'Ô tìm nhanh tìm theo mã phiếu, số hợp đồng, mã / tên ' + o, 'P0',
         'Có 19 khai báo của ' + c['obj_sample'] + '.',
         nl('1. Gõ "KIM LONG" vào ô tìm nhanh (chưa bấm gì).' if not is_ncc else '1. Gõ "FLY" vào ô tìm nhanh (chưa bấm gì).',
            '2. Bấm Enter.', '3. Lần lượt tìm theo một mã phiếu và một số hợp đồng.'),
         'Tìm nhanh: KIM LONG' if not is_ncc else 'Tìm nhanh: FLY',
         nl('- Đang gõ thì bảng chưa đổi; Enter hoặc nút Tìm kiếm mới lọc.',
            '- Ra đúng các khai báo của ' + o + ' có tên chứa từ khoá.',
            '- Tìm theo mã phiếu / số hợp đồng ra đúng khai báo chứa chuỗi đó.',
            '- Placeholder ghi "Tìm theo mã phiếu, số hợp đồng, mã hoặc tên ' + o + '".',
            '- Đối chiếu ERP: ERP không có ô tìm nhanh, phải lọc từng ô.')),
        ('002', 'Lọc theo ' + O + ' (gõ để tìm)', 'P0',
         O + ' ' + c['obj_sample'] + ' có khai báo.',
         nl('1. Mở Tìm kiếm nâng cao.', '2. Ô ' + O + ' gõ 1 ký tự, rồi gõ "' + c['obj_code'] + '".',
            '3. Chọn ' + o + ' trong danh sách gợi ý.'),
         O + ': ' + c['obj_code'],
         nl('- Gõ 1 ký tự: báo cần gõ thêm, chưa tìm.', '- Chọn xong bảng tự lọc, chỉ còn khai báo của ' + o + ' đó.',
            '- F5 lại trang: ô ' + O + ' vẫn hiện đúng tên đã chọn.')),
        ('003', 'Lọc theo Tài khoản', 'P1',
         'Mọi khai báo hiện có đều dùng tài khoản ' + c['account_no'] + '.',
         nl('1. Ô Tài khoản chọn "' + acc + '".', '2. Đổi sang một tài khoản khác.'),
         'Tài khoản: ' + acc,
         nl('- Chọn ' + c['account_no'] + ': ra toàn bộ khai báo trong phạm vi.', '- Tài khoản khác: "Không có dữ liệu phù hợp bộ lọc."')),
        ('004', 'Lọc theo Loại hợp đồng', 'P1',
         'Có khai báo gắn ' + c['contract_type'] + '.',
         nl('1. Ô Loại hợp đồng chọn "' + (c['contract_type'] if is_ncc else 'Hợp đồng đầu kỳ') + '".'),
         'Loại hợp đồng: ' + (c['contract_type'] if is_ncc else 'Hợp đồng đầu kỳ'),
         nl('- Chỉ còn khai báo gắn đúng loại hợp đồng đó, cột Loại hợp đồng (bật thêm) đúng tên loại.',
            '- Đối chiếu ERP: ERP không có ô lọc này.')),
        ('005', 'Lọc theo Số hợp đồng', 'P1',
         'Có khai báo gắn hợp đồng ' + c['contract_sample'] + '.',
         nl('1. Ô Số hợp đồng gõ một phần số hợp đồng.', '2. Bấm Enter.'),
         'Số hợp đồng: một phần của ' + c['contract_sample'],
         nl('- Chờ Enter mới lọc.', '- Ra khai báo có số hợp đồng chứa chuỗi đã gõ, với MỌI loại hợp đồng.',
            '- Đối chiếu ERP: ERP lọc sót một số loại hợp đồng (vd ' +
            ('hợp đồng mua trong nước mới' if is_ncc else 'hợp đồng dịch vụ bảo hành') + ') — HRM tìm được hết.')),
        ('006', 'Lọc theo Loại dư', 'P0',
         ('Dữ liệu thật: 1,175 khai báo Dư nợ trên tổng 1,746.' if not is_ncc else 'Có cả khai báo Dư nợ và Dư có.'),
         nl('1. Ô Loại dư chọn "Dư nợ".', '2. Đổi sang "Dư có".'),
         'Loại dư: Dư nợ / Dư có',
         nl('- Chọn là lọc ngay.', '- Dư nợ: mọi dòng chỉ có số ở cột Dư nợ.', '- Dư có: mọi dòng chỉ có số ở cột Dư có.')),
        ('007', 'Lọc theo khoảng Công nợ', 'P1',
         'Có khai báo 1,500,000 và 10,125,000.',
         nl('1. Ô Công nợ nhập Từ 1,000,000, Đến 5,000,000.', '2. Bấm Enter.'),
         'Công nợ từ 1,000,000 đến 5,000,000',
         nl('- Chỉ còn khai báo có số tiền trong khoảng (tính cả 2 đầu).', '- Không có 10,125,000.')),
        ('008', 'Lọc theo Người tạo / Người cập nhật', 'P2',
         'Nhân viên Nguyễn Thị Thu Trang tạo nhiều khai báo.',
         nl('1. Ô Người tạo chọn Nguyễn Thị Thu Trang.', '2. Xoá, rồi ô Người cập nhật chọn cùng người.'),
         '—',
         nl('- Chỉ còn khai báo do người đó tạo / cập nhật lần cuối.')),
        ('009', 'Lọc theo Ngày tạo (khoảng)', 'P1',
         'Có 1 khai báo tạo trong tháng 12/2025.',
         nl('1. Ô Ngày tạo chọn từ 01/12/2025 đến 31/12/2025.'),
         'Ngày tạo: từ 01/12/2025 đến 31/12/2025',
         nl('- Ra đúng 1 khai báo.', '- Khai báo tạo lúc 23:59 ngày 31/12/2025 vẫn được tính.')),
        ('010', 'Lọc theo Công ty / Phòng ban / Bộ phận', 'P1',
         'Tài khoản có quyền "Xem tất cả công nợ đầu kỳ".',
         nl('1. Ô Công ty chọn TPE.', '2. Ô Phòng ban chọn một phòng.'),
         '—',
         nl('- Mỗi ô chọn xong là lọc ngay.', '- Đổi Công ty thì Phòng ban, Bộ phận tự xoá.')),
        ('011', 'Làm mới xoá hết điều kiện và tải lại', 'P1',
         'Đang lọc theo Loại dư = Dư nợ và từ khoá "KIM LONG".',
         nl('1. Bấm Làm mới.'),
         '—',
         nl('- Mọi ô lọc về trống, bảng nạp lại toàn bộ phạm vi.')),
        ('012', 'Ghi nhớ bộ lọc khi vào chi tiết rồi quay lại', 'P1',
         'Đang lọc Loại dư = Dư có, đang ở trang 2.',
         nl('1. Bấm vào một mã phiếu.', '2. Bấm Quay lại.'),
         '—',
         nl('- Bộ lọc vẫn còn Loại dư = Dư có.')),
    ]
    if is_ncc:
        S2 += [
            ('013', 'Lọc theo Loại tiền', 'P1',
             'Dữ liệu thật: 225 khai báo USD.',
             nl('1. Ô Loại tiền chọn USD.'), 'Loại tiền: USD',
             nl('- Chỉ còn khai báo USD; cột Loại tiền đều ghi USD.')),
            ('014', 'Lọc theo Người lập hợp đồng', 'P2',
             'Có khai báo của hợp đồng do Nguyễn Thị Ngoan lập.',
             nl('1. Ô Người lập hợp đồng chọn Nguyễn Thị Ngoan.'), '—',
             nl('- Chỉ còn khai báo có Người lập hợp đồng là người đó.', '- Đối chiếu ERP: có ô lọc này, giữ nguyên.')),
        ]

    S3 = [
        ('001', 'Sắp xếp theo Mã phiếu và Ngày tạo', 'P1', 'Có hơn 20 khai báo.',
         nl('1. Bấm tiêu đề cột Mã phiếu.', '2. Bấm lần nữa.', '3. Bấm tiêu đề cột Ngày tạo.'),
         '—',
         nl('- Mã phiếu tăng dần rồi giảm dần.', '- Bấm Ngày tạo thì bỏ sắp xếp Mã phiếu, sắp theo ngày.')),
        ('002', 'Phân trang và số dòng / trang', 'P1', 'Có {n} khai báo.'.format(n=c['total_company']),
         nl('1. Sang trang 3.', '2. Đổi số dòng/trang sang 50.'),
         '—',
         nl('- Trang 3 STT bắt đầu từ 21.', '- Đổi 50 dòng thì quay về trang 1, "Hiển thị 1–50 / {n}".'.format(n=c['total_company']),
            '- Lựa chọn số dòng: 5 / 10 / 20 / 50 / 100.')),
        ('003', 'Cấu hình cột hiển thị được ghi nhớ', 'P2', '—',
         nl('1. Bấm biểu tượng Cấu hình cột.', '2. Bật cột Tài khoản, Ngày tính công nợ, lưu.', '3. F5 trang.'),
         '—',
         nl('- 2 cột mới hiện; sau F5 vẫn còn.', '- Không tắt được cột STT, Mã phiếu, Hành động.')),
        ('004', 'Nút Sửa / Xóa ẩn với khai báo đã phát sinh chứng từ', 'P0',
         nl('Khai báo Y đã có phiếu thu / phiếu kế toán trên cùng hợp đồng + tài khoản.',
            'Khai báo Z mới tạo, hợp đồng chưa có chứng từ công nợ nào.'),
         nl('1. Tìm 2 dòng Y và Z.'),
         '—',
         nl('- Dòng Y chỉ có nút Lịch sử, KHÔNG có Sửa / Xóa (ẩn hẳn, không hiện xám).',
            '- Dòng Z có Sửa, Xóa, Lịch sử.',
            '- Đối chiếu ERP: ' + ('ERP luôn hiện Sửa / Xóa ở màn khách hàng.' if not is_ncc
                                  else 'ERP tính MỌI chứng từ khác (cả phiếu nhập hàng); HRM chỉ tính chứng từ công nợ.'))),
        ('005', 'Phiếu xuất hàng KHÔNG làm khoá khai báo', 'P0',
         nl('Hợp đồng ' + c['contract_sample'] + ' đã có phiếu ' + ('xuất' if not is_ncc else 'nhập') +
            ' hàng ghi sổ tài khoản ' + c['account_no'] + ', chưa có phiếu thu/chi/kế toán.',
            'Vừa tạo khai báo trên hợp đồng này.'),
         nl('1. Mở danh sách, tìm khai báo vừa tạo.'),
         '—',
         nl('- Vẫn có nút Sửa, Xóa.',
            '- Lưu ý: nếu sau đó lập phiếu thu / phiếu kế toán cho hợp đồng này thì nút Sửa / Xóa biến mất.')),
    ]

    contract_col = 'Loại hợp đồng, Số hợp đồng' + (', Người lập hợp đồng' if is_ncc else '')
    row_cols = 'Tài khoản, ' + ('Loại tiền, Tỷ giá, ' if is_ncc else '') + 'Loại dư, Công nợ' + (', Quy đổi (VND)' if is_ncc else '')
    S4 = [
        ('001', 'Mở màn Thêm mới', 'P0', 'Tài khoản đủ quyền thêm.',
         nl('1. Bấm Tạo mới.'),
         '—',
         nl('- Tiêu đề "Thêm {t}".'.format(t=c['title'].lower()),
            '- Khối "Thông tin chung" có ô ' + O + ' (bắt buộc).',
            '- Khối "Danh sách hợp đồng' + (' mua' if is_ncc else '') + '" có nút "Chọn hợp đồng", bảng trống ghi '
            '"Chưa chọn hợp đồng nào — bấm \"Chọn hợp đồng\" để thêm.".',
            '- Cột bảng: STT, ' + contract_col + ', ' + row_cols + ', nút xoá dòng.',
            '- Chân trang: Lưu, Quay lại.',
            '- Đối chiếu ERP: ERP dùng cửa sổ nổi; HRM là trang riêng, nội dung các ô giữ nguyên.')),
        ('002', 'Chưa chọn ' + o + ' thì không mở được cửa sổ chọn hợp đồng', 'P0', '—',
         nl('1. Bấm "Chọn hợp đồng" khi ô ' + O + ' còn trống.'),
         '—',
         nl('- Không mở cửa sổ.', '- Báo đỏ dưới ô ' + O + ': "Chọn ' + o + ' trước khi chọn hợp đồng".')),
        ('003', 'Ô ' + O + ' tìm từ máy chủ', 'P1', O + ' ' + c['obj_sample'] + '.',
         nl('1. Gõ 1 ký tự.', '2. Gõ "' + c['obj_code'] + '".'),
         O + ': ' + c['obj_code'],
         nl('- Dưới 2 ký tự: báo cần gõ thêm.', '- Gợi ý dạng "Mã - Tên"' + (', chỉ nhà cung cấp đang hoạt động.' if is_ncc else '.'))),
        ('004', 'Cửa sổ chọn hợp đồng: danh sách và tình trạng', 'P0',
         nl(O + ' ' + c['obj_sample'] + ' có ' + ('27 hợp đồng, 1 hợp đồng đầu kỳ đã khai báo.' if not is_ncc
                                                   else 'nhiều hợp đồng mua, có hợp đồng đã khai báo.')),
         nl('1. Chọn ' + o + ', bấm "Chọn hợp đồng".'),
         '—',
         nl('- Tiêu đề "' + ('Chọn hợp đồng / đơn hàng' if not is_ncc else 'Chọn hợp đồng mua') + '", dòng phụ ghi tên ' + o + '.',
            '- Cột: STT, Loại hợp đồng, Số hợp đồng, Tổng thanh toán, Người tạo, Ngày tạo, Tình trạng.',
            '- Hợp đồng đã khai báo: dòng mờ, Tình trạng "Đã khai báo".',
            '- Có ô lọc ' + ('Phạm vi, ' if is_ncc else '') + 'Loại hợp đồng, Số hợp đồng; nút Tìm kiếm, Làm mới; phân trang.')),
        ('005', 'Bấm vào dòng là thêm hợp đồng ngay', 'P0', 'Đang mở cửa sổ chọn hợp đồng.',
         nl('1. Bấm vào dòng hợp đồng ' + c['contract_sample'] + '.', '2. Bấm thêm một dòng khác.',
            '3. Bấm lại dòng đầu.', '4. Bấm một dòng "Đã khai báo".', '5. Bấm Đóng.'),
         '—',
         nl('- Mỗi lần bấm hiện thông báo "Đã thêm hợp đồng <số hợp đồng>", cửa sổ vẫn mở để chọn tiếp.',
            '- Dòng đã chọn chuyển sang "Đã chọn", bấm lại không thêm trùng.',
            '- Dòng "Đã khai báo" bấm không có tác dụng.',
            '- Đóng cửa sổ: bảng có đúng 2 dòng.',
            '- Đối chiếu ERP: ' + ('ERP chỉ báo trùng khi bấm Lưu; HRM chặn ngay trong cửa sổ.' if not is_ncc else 'giống ERP (báo trùng ngay khi chọn).'))),
        ('006', 'Lọc trong cửa sổ chọn hợp đồng', 'P1', 'Đang mở cửa sổ.',
         nl('1. Loại hợp đồng chọn "' + (c['contract_type'] if is_ncc else 'Hợp đồng đầu kỳ') + '".',
            '2. Số hợp đồng gõ một phần số, Enter.', '3. Bấm Làm mới.'),
         '—',
         nl('- Chỉ còn hợp đồng đúng loại / chứa chuỗi.', '- Làm mới về toàn bộ hợp đồng.')),
    ]
    if not is_ncc:
        S4 += [
            ('007', 'Đủ 8 nguồn hợp đồng như ERP, luôn đúng khách hàng', 'P0',
             'Khách hàng có hợp đồng bán, hợp đồng hãng, hợp đồng đầu kỳ.',
             nl('1. Mở cửa sổ chọn hợp đồng.', '2. Lần lượt chọn từng Loại hợp đồng trong danh sách.'),
             '—',
             nl('- Có đủ lựa chọn: Hợp đồng hãng, Hợp đồng, Đơn hàng, Hợp đồng nguyên tắc, Hợp đồng thúc đẩy bán, '
                'Đơn hàng thúc đẩy bán, Phụ lục bổ sung, Phụ lục HĐNT, Hợp đồng gói dịch vụ, Hợp đồng dự án, '
                'Hợp đồng đầu kỳ, Hợp đồng mua nước ngoài, Hợp đồng mua ngoài, Hợp đồng mua trong nước.',
                '- Mọi kết quả đều thuộc khách hàng đang chọn.',
                '- Để trống Loại hợp đồng: gộp tất cả các nguồn.',
                '- Đối chiếu ERP: ERP để trống chỉ ra hợp đồng bán; "Hợp đồng mua nước ngoài" luôn rỗng; '
                '"Hợp đồng mua ngoài" ra hợp đồng của MỌI đối tượng; "Hợp đồng dự án / đầu kỳ" chỉ ra hợp '
                'đồng do chính mình tạo — HRM đã sửa cả 4 lỗi.')),
            ('008', 'Chỉ hợp đồng còn hiệu lực', 'P1',
             'Khách hàng có 1 hợp đồng bán Đang tạo và 1 hợp đồng hãng đã thanh lý.',
             nl('1. Mở cửa sổ chọn hợp đồng.'), '—',
             nl('- Không thấy 2 hợp đồng trên.', '- Hợp đồng bán chỉ hiện khi Đã duyệt / Có hiệu lực; hợp đồng hãng chỉ khi Có hiệu lực.')),
        ]
    else:
        S4 += [
            ('007', 'Phạm vi: hợp đồng của nhà cung cấp khác', 'P0',
             'Nhà cung cấp FLY; có hợp đồng mua của nhà cung cấp khác.',
             nl('1. Mở cửa sổ chọn hợp đồng.', '2. Ô Phạm vi chọn "Hợp đồng của nhà cung cấp khác".'),
             '—',
             nl('- Bảng thêm cột Nhà cung cấp, chỉ hiện hợp đồng KHÔNG thuộc FLY.',
                '- Chọn được và lưu được (giữ như tab "HĐ Nhà cung cấp khác" của ERP).')),
            ('008', 'Thêm hợp đồng mua ngoại tệ tự điền Loại tiền, Tỷ giá, Người lập', 'P0',
             'Hợp đồng ' + c['contract_sample'] + ' là hợp đồng mua nước ngoài bằng USD, do Nguyễn Thị Ngoan (12210335) lập.',
             nl('1. Chọn hợp đồng ' + c['contract_sample'] + '.', '2. Đóng cửa sổ, đọc dòng vừa thêm.'),
             '—',
             nl('- Người lập hợp đồng: "12210335 - Nguyễn Thị Ngoan".', '- Loại tiền: USD.',
                '- Tỷ giá tự điền theo tỷ giá đang khai ở danh mục tiền tệ (sửa được).',
                '- Loại dư mặc định Dư nợ; Tài khoản lấy theo dòng phía trên (nếu có).')),
        ]
    n = len(S4)
    S4 += [
        ('%03d' % (n + 1), 'Lưu thành công nhiều hợp đồng', 'P0',
         'Đã chọn 2 hợp đồng của ' + c['obj_sample'] + '.',
         nl('1. Dòng 1: Tài khoản ' + c['account_no'] + ', Dư nợ, Công nợ 1,500,000' + (', Tỷ giá 25,450.5' if is_ncc else '') + '.',
            '2. Dòng 2: Tài khoản ' + c['account_no'] + ', Dư có, Công nợ 5.', '3. Bấm Lưu.'),
         nl('Dòng 1: ' + acc + ' / Dư nợ / 1,500,000', 'Dòng 2: ' + acc + ' / Dư có / 5'),
         nl('- Thông báo "Thêm mới thành công.", quay về danh sách.',
            '- Danh sách có 2 khai báo mới, mã nối tiếp dạng ' + c['code_sample'] + '.',
            '- Ngày tính công nợ của cả 2 là 01/08/2025.',
            '- Bên ERP mở báo cáo sổ chi tiết công nợ: có 2 bút toán ' + ('Nợ' + ' / Có') + ' tài khoản ' + c['account_no'] + ' tương ứng.')),
        ('%03d' % (n + 2), 'Bấm Lưu khi chưa nhập đủ', 'P0', 'Đã chọn 2 hợp đồng, chưa nhập gì.',
         nl('1. Bấm Lưu.'), '—',
         nl('- Thông báo "Bạn chưa nhập đầy đủ thông tin.", ở lại form.',
            '- Dưới ô Tài khoản và ô Công nợ của TỪNG dòng báo đỏ "Bắt buộc phải nhập".',
            '- Màn tự cuộn tới dòng lỗi đầu tiên và tô nền đỏ nhạt dòng đó.')),
        ('%03d' % (n + 3), 'Xoá dòng trên form', 'P1', 'Đã chọn 3 hợp đồng, dòng 3 đang báo lỗi.',
         nl('1. Bấm nút xoá ở dòng 1.'), '—',
         nl('- Còn 2 dòng; lỗi vẫn nằm đúng dòng (nay là dòng 2), dòng khác không nhận lỗi oan.',
            '- Hợp đồng vừa xoá chọn lại được trong cửa sổ.')),
        ('%03d' % (n + 4), 'Đổi ' + o + ' thì danh sách hợp đồng bị xoá', 'P1', 'Đã chọn 2 hợp đồng.',
         nl('1. Đổi ô ' + O + ' sang ' + o + ' khác.'), '—',
         nl('- Bảng hợp đồng về trống (hợp đồng gắn theo ' + o + ').')),
        ('%03d' % (n + 5), 'Cảnh báo khi thoát lúc chưa lưu', 'P1', 'Đã chọn 1 hợp đồng, đã nhập Công nợ.',
         nl('1. Bấm Quay lại.', '2. Bấm "Ở lại".', '3. Bấm Quay lại lần nữa, bấm "Thoát".'), '—',
         nl('- Hiện hộp "Thông tin chưa lưu" với câu "Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?".',
            '- Ở lại: giữ nguyên dữ liệu.', '- Thoát: về danh sách, không lưu gì.')),
    ]

    S5 = [
        ('001', 'Màn Chi tiết', 'P0', 'Khai báo ' + c['code_sample'] + ' của ' + c['obj_sample'] + '.',
         nl('1. Bấm vào mã phiếu.'), '—',
         nl('- Tiêu đề "Chi tiết {t}: {c}".'.format(t=c['title'].lower(), c=c['code_sample']),
            '- Khối Thông tin chung: Mã phiếu, ' + O + ', Ngày tính công nợ (01/08/2025) — đều khoá.',
            '- Bảng đúng 1 dòng, các ô khoá.', '- Có khối "Lịch sử" đang thu gọn.',
            '- Chân trang: Sửa, Xóa (nếu chưa phát sinh và có quyền), Quay lại.')),
        ('002', 'Nút ở Chi tiết khớp với dòng ở danh sách', 'P0',
         'Khai báo Y đã phát sinh chứng từ; khai báo Z chưa.',
         nl('1. Mở chi tiết Y.', '2. Mở chi tiết Z.'), '—',
         nl('- Y: chỉ có Quay lại.', '- Z: Sửa, Xóa, Quay lại — giống hệt nút ở dòng danh sách.')),
        ('003', 'Sửa: chỉ sửa được tài khoản, loại dư, công nợ' + (', loại tiền, tỷ giá' if is_ncc else ''), 'P0',
         'Khai báo Z chưa phát sinh.',
         nl('1. Bấm Sửa.', '2. Đổi Loại dư sang Dư có, Công nợ 2,750,000.5' + (', Loại tiền VNĐ' if is_ncc else '') + '.', '3. Bấm Lưu.'),
         nl('Loại dư: Dư có', 'Công nợ: 2,750,000.5'),
         nl('- Ô ' + O + ' và hợp đồng bị khoá.', '- Thông báo "Cập nhật thành công.", về danh sách.',
            '- Danh sách: Dư có 2,750,000.5.',
            '- Sổ: bút toán đổi sang Có, số tiền 2,750,000.5, quy đổi 2,750,001.'
            + ('\n- Đổi sang VNĐ thì Tỷ giá tự về 1 và khoá; Quy đổi = Công nợ.' if is_ncc else ''),
            '- Đối chiếu ERP: ERP đổi tài khoản thì sổ vẫn giữ SỐ tài khoản cũ — HRM cập nhật đúng.')),
        ('004', 'Sửa sang tài khoản đã khai báo cho cùng hợp đồng bị chặn', 'P1',
         'Hợp đồng H của ' + o + ' đã có khai báo tài khoản A và khai báo tài khoản B.',
         nl('1. Sửa khai báo tài khoản B, đổi sang tài khoản A.', '2. Bấm Lưu.'), '—',
         nl('- Báo đỏ dưới ô Tài khoản: "Đã khai báo đầu kỳ cho tài khoản này".',
            '- Đối chiếu ERP: ERP không kiểm, tạo được 2 khai báo trùng.')),
        ('005', 'Vào thẳng màn Sửa của khai báo đã phát sinh', 'P0', 'Khai báo Y đã phát sinh chứng từ.',
         nl('1. Dán đường dẫn màn Sửa của Y.'), '—',
         nl('- Thông báo "Khai báo đã phát sinh chứng từ hoặc bạn không có quyền sửa.".',
            '- Tự chuyển về màn Chi tiết của Y.')),
        ('006', 'Lịch sử thay đổi ở Chi tiết', 'P0', 'Khai báo Z vừa tạo rồi sửa 1 lần.',
         nl('1. Mở chi tiết Z.', '2. Bấm "Xem lịch sử".'), '—',
         nl('- Mới nhất ở trên: "Thay đổi thông tin" — Loại dư: Dư nợ thành Dư có; Công nợ: 1,500,000.00 thành 2,750,000.50 (cũ đỏ, mới xanh).',
            '- Dưới cùng: "Tạo mới" kèm người thực hiện và phòng ban.',
            '- Bộ lọc lịch sử: Loại hành động (Tạo mới / Thay đổi thông tin / Thay đổi trạng thái), Người thực hiện, Từ ngày, Đến ngày.',
            '- Đối chiếu ERP: ERP không có lịch sử.')),
        ('007', 'Lịch sử mở từ danh sách', 'P1', 'Khai báo Z như trên.',
         nl('1. Ở danh sách, bấm nút Lịch sử của dòng Z.'), '—',
         nl('- Cửa sổ "Lịch sử" tiêu đề kèm mã phiếu Z, nội dung giống hệt khối ở Chi tiết.')),
    ]

    S6 = [
        ('001', 'Xóa khai báo chưa phát sinh', 'P0', 'Khai báo Z chưa phát sinh chứng từ.',
         nl('1. Bấm Xóa ở dòng Z.', '2. Bấm Hủy.', '3. Bấm Xóa lần nữa, bấm Xóa trong hộp xác nhận.'), '—',
         nl('- Hộp xác nhận "Bạn có chắc muốn xóa bản ghi này không?".', '- Hủy: không đổi gì.',
            '- Xóa: thông báo "Xóa thành công.", dòng biến mất.',
            '- Bên ERP: bút toán của Z không còn trong sổ chi tiết công nợ.')),
        ('002', 'Xóa từ màn Chi tiết', 'P1', 'Khai báo Z chưa phát sinh.',
         nl('1. Mở chi tiết Z, bấm Xóa, xác nhận.'), '—',
         nl('- Về danh sách, Z không còn.')),
        ('003', 'Không xóa được khai báo đã phát sinh', 'P0', 'Khai báo Y đã phát sinh.',
         nl('1. Tìm dòng Y ở danh sách và mở chi tiết.'), '—',
         nl('- Không có nút Xóa ở cả 2 nơi.',
            '- Đối chiếu ERP: ' + ('ERP xoá được, làm lệch báo cáo công nợ đã có phiếu thu.' if not is_ncc
                                  else 'ERP ẩn nút nhưng vẫn xoá được nếu gọi thẳng.'))),
    ]

    imp_cols = ('Mã khách hàng, Mã hợp đồng, Loại hợp đồng, Số tài khoản, Loại dư, Công nợ' if not is_ncc else
                'Nhà cung cấp, Mã hợp đồng mua, Loại hợp đồng mua, Số tài khoản, Loại tiền, Tỷ giá, Loại dư, Công nợ')
    codes = ('HDDK (đầu kỳ), HDHNTDA (hãng/dự án), HDDV (dịch vụ BH-SC), HDMNN, HDMN, HDMTN (hợp đồng mua)' if not is_ncc
             else 'HDMNN (mua nước ngoài), HDMN (mua ngoài), HDMTN (mua trong nước), HDMDK (mua đầu kỳ)')
    S7 = [
        ('001', 'Tải file mẫu', 'P1', '—',
         nl('1. Bấm Import Excel.', '2. Bấm tải file mẫu, mở file.'), '—',
         nl('- File có cột STT rồi: ' + imp_cols + ' (giữ thứ tự file mẫu ERP).',
            '- Hàng 1 tiêu đề nền xanh nhạt, cột bắt buộc có dấu *; hàng 2 mô tả in nghiêng; hàng 3 dòng ví dụ.',
            '- Cột Loại hợp đồng và Loại dư bấm ra danh sách chọn.')),
        ('002', 'Kiểm tra dữ liệu import', 'P0', 'File 3 dòng: 1 dòng đúng, 1 dòng trùng dòng trên, 1 dòng sai mọi cột.',
         nl('1. Chọn file, bấm kiểm tra.'), '—',
         nl('- Dòng đúng: xanh, khoá.', '- Dòng trùng: "Trùng với dòng 1 trong file".',
            '- Dòng sai báo từng lỗi: "' + O + ' – Mã không tồn tại trong hệ thống", "Loại hợp đồng – Chỉ nhận ...", '
            '"Số tài khoản – Không tồn tại trong hệ thống", "Loại dư – Chỉ nhận \"Dư nợ\" hoặc \"Dư có\"", "Công nợ – Phải lớn hơn 0."',
            '- Sửa được dòng lỗi ngay trên bảng rồi kiểm lại.')),
        ('003', 'Import chỉ lấy dòng hợp lệ', 'P0', 'Sau TC_07.002: 1 hợp lệ, 2 lỗi.',
         nl('1. Bấm Import.'), '—',
         nl('- Thông báo import thành công 1 khai báo; cửa sổ đóng, danh sách nạp lại.',
            '- Khai báo mới có mã phiếu nối tiếp và có bút toán trong sổ như khi lập tay.',
            '- Đối chiếu ERP: ERP còn 1 dòng lỗi là không lưu dòng nào.')),
        ('004', 'Import kiểm hợp đồng tồn tại' + (' và thuộc khách hàng' if not is_ncc else ''), 'P0',
         'File: mã hợp đồng không có thật; ' + ('mã hợp đồng của khách hàng khác.' if not is_ncc else 'mã hợp đồng đúng.'),
         nl('1. Kiểm tra file.'), '—',
         nl('- "Mã hợp đồng – Không tồn tại trong hệ thống".'
            + ('\n- "Mã hợp đồng – Không thuộc khách hàng này".' if not is_ncc else ''),
            '- Đối chiếu ERP: ' + ('ERP không kiểm, hợp đồng sai làm màn treo lỗi.' if not is_ncc else 'giống ERP (có kiểm tồn tại).'))),
        ('005', 'Mã loại hợp đồng được nhận', 'P1', 'File dùng lần lượt các mã: ' + codes + '.',
         nl('1. Kiểm tra file.'), '—',
         nl('- Đúng các mã trên được nhận; mã khác báo "Loại hợp đồng – Chỉ nhận ...".')),
        ('006', 'Import trùng khai báo đã có', 'P1', 'Hợp đồng H + tài khoản ' + c['account_no'] + ' đã khai báo cho ' + o + ' X.',
         nl('1. File có dòng X + H + ' + c['account_no'] + '.', '2. Kiểm tra.'), '—',
         nl('- "Hợp đồng đã được khai báo công nợ đầu kỳ cho tài khoản này".')),
    ]
    if is_ncc:
        S7.append(('007', 'Import loại tiền, tỷ giá', 'P1', 'File: dòng USD không có tỷ giá; dòng "VNĐ" và dòng "VND" không có tỷ giá.',
                   nl('1. Kiểm tra file.'), '—',
                   nl('- USD không tỷ giá: "Tỷ giá – Bắt buộc phải nhập".', '- VNĐ / VND: hợp lệ, tỷ giá 1.')))

    S8 = [
        ('001', 'Xuất Excel: chọn trường trước khi xuất', 'P0', 'Đang lọc theo từ khoá "' + c['obj_code'] + '".',
         nl('1. Bấm Xuất Excel.', '2. Xem các trường được tích sẵn.', '3. Bỏ tích Người tạo, kéo Dư có lên trên Dư nợ, bấm Xuất file.'), '—',
         nl('- Hộp "Chọn trường xuất file" tích sẵn đúng các cột đang hiện trên bảng.',
            '- Có dòng tiến độ cạnh nút trong lúc xuất; xong báo "Xuất Excel thành công".',
            '- File chỉ có các dòng khớp bộ lọc, cột theo đúng thứ tự đã kéo.',
            '- Cột Dư nợ / Dư có là SỐ (cộng được bằng SUM), định dạng 1,234,567.')),
        ('002', 'In danh sách', 'P0', 'Đang lọc theo từ khoá "' + c['obj_code'] + '".',
         nl('1. Bấm In danh sách.'), '—',
         nl('- Cửa sổ xem trước khổ NGANG, có logo công ty, tiêu đề "' + c['print_title'] + '" (mẫu in dùng chung với ERP).',
            '- Bảng in đúng các cột đang hiện trên màn, đúng các dòng khớp bộ lọc.',
            '- Số có phần lẻ giữ phần lẻ (2,750,000.5).', '- Bấm In mở hộp in của trình duyệt.')),
        ('003', 'In danh sách quá 2,000 dòng', 'P1', 'Không lọc gì, phạm vi có hơn 2,000 khai báo.',
         nl('1. Bấm In danh sách.'), '—',
         nl('- Không in; báo "Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được..." và gợi ý thu hẹp bộ lọc hoặc dùng Xuất Excel.')),
    ]

    S9 = [
        ('001', 'Trùng hợp đồng + tài khoản trên cùng form', 'P0',
         'Hợp đồng H đã có trên form (đang chọn 1 lần).', nl('1. Thử chọn lại H trong cửa sổ.'), '—',
         nl('- Không thêm được (dòng "Đã chọn").')),
        ('002', 'Trùng với khai báo đã có', 'P0', 'Hợp đồng H + tài khoản ' + c['account_no'] + ' đã khai báo; H được chọn qua cách khác (vd 2 người lập song song).',
         nl('1. Người thứ 2 bấm Lưu.'), '—',
         nl('- Báo đỏ dưới ô Tài khoản: "Đã khai báo đầu kỳ cho tài khoản này".', '- Không lưu dòng nào trong lần đó.')),
        ('003', 'Công nợ bằng 0 hoặc để trống', 'P0', '—',
         nl('1. Để trống Công nợ, Lưu.', '2. Nhập 0, Lưu.'), '—',
         nl('- Trống: "Bắt buộc phải nhập".', '- 0: "Phải lớn hơn 0."', '- Ô tiền không cho gõ dấu âm.')),
        ('004', 'Tài khoản không thuộc danh sách', 'P1', '— (tester kỹ thuật)',
         nl('1. Gọi thẳng chức năng Thêm với một tài khoản tổng hợp (có tài khoản con) hoặc tài khoản đang khoá.'), '—',
         nl('- Báo "Tài khoản không hợp lệ" ở đúng dòng.')),
        ('005', 'Hợp đồng không thuộc ' + o + ' / không tồn tại', 'P0' if not is_ncc else 'P1', '— (tester kỹ thuật)',
         nl('1. Gọi thẳng chức năng Thêm với hợp đồng của đối tượng khác và hợp đồng không có thật.'), '—',
         nl(('- Hợp đồng của khách hàng khác: "Hợp đồng không thuộc khách hàng đã chọn".\n' if not is_ncc else
             '- Hợp đồng của nhà cung cấp khác: được nhận (giữ như ERP).\n') +
            '- Hợp đồng không có thật: "Hợp đồng không tồn tại".')),
    ]
    if is_ncc:
        S9.append(('006', 'Tỷ giá khi khác VNĐ', 'P0', 'Dòng USD.',
                   nl('1. Xoá trống ô Tỷ giá, Lưu.', '2. Nhập 0, Lưu.'), '—',
                   nl('- Trống: "Bắt buộc phải nhập" dưới ô Tỷ giá.', '- 0: báo lỗi phải lớn hơn 0.',
                      '- Đối chiếu ERP: ERP nhận tỷ giá tối thiểu 1; HRM nhận số thập phân lớn hơn 0.')))

    S10 = [
        ('001', 'Mã phiếu không trùng khi 2 người lưu cùng lúc', 'P1', '2 tài khoản cùng công ty.',
         nl('1. Hai người cùng lập khai báo, bấm Lưu gần như đồng thời.'), '—',
         nl('- 2 khai báo có 2 mã nối tiếp, không trùng, không lỗi.',
            '- Đối chiếu ERP: ERP màn khách hàng có 2 cách sinh mã chạy song song nên từng bị trùng mã.')),
        ('002', 'Khai báo vừa phát sinh chứng từ trong lúc người khác đang sửa', 'P1',
         'A đang mở màn Sửa khai báo Z; B lập phiếu thu cho hợp đồng của Z.',
         nl('1. A bấm Lưu.'), '—',
         nl('- A bị từ chối với câu "Khai báo đã phát sinh chứng từ, không được sửa / xóa.", dữ liệu không đổi.')),
        ('003', 'Dữ liệu lập bên HRM hiện bên ERP và ngược lại', 'P0', '—',
         nl('1. Lập 1 khai báo bên HRM.', '2. Mở màn tương ứng bên ERP.', '3. Lập 1 khai báo bên ERP, mở lại HRM.'), '—',
         nl('- Khai báo của HRM hiện bên ERP đúng ' + o + ', hợp đồng, số tiền.',
            '- Khai báo của ERP hiện bên HRM, mã phiếu tiếp tục nối tiếp.')),
    ]

    S11 = [
        ('001', 'Luồng đầu cuối: khai báo, ' + ('thu tiền' if not is_ncc else 'chi tiền') + ', rồi bị khoá sửa / xoá', 'P0',
         nl(O + ' ' + c['obj_sample'] + ' có hợp đồng ' + c['contract_sample'] + ' chưa khai báo.'),
         nl('1. Lập khai báo ' + ('Dư nợ 1,500,000' if not is_ncc else 'Dư có 1,000.25 USD tỷ giá 25,450.5') + ', tài khoản ' + c['account_no'] + '.',
            '2. Mở sổ chi tiết công nợ bên ERP, tìm bút toán.',
            '3. Lập ' + ('phiếu thu' if not is_ncc else 'phiếu chi / ủy nhiệm chi') + ' cho hợp đồng này (ghi sổ tài khoản ' + c['account_no'] + ').',
            '4. Quay lại danh sách khai báo.'), '—',
         nl('- Bước 2: sổ có bút toán ' + ('Nợ 1311 1,500,000' if not is_ncc else 'Có 3311 nguyên tệ 1,000.25, quy đổi 25,456,863') + ', ngày 01/08/2025, chứng từ là mã phiếu khai báo.',
            '- Bước 4: dòng khai báo không còn nút Sửa, Xóa; chi tiết chỉ còn Quay lại.')),
        ('002', 'Luồng đầu cuối: import, sửa, rồi xoá', 'P1', 'File import 1 dòng hợp lệ.',
         nl('1. Import.', '2. Sửa số tiền.', '3. Xóa.', '4. Xem Lịch sử trước khi xoá.'), '—',
         nl('- Mỗi bước sổ đổi theo; xoá xong sổ không còn bút toán.',
            '- Lịch sử có đủ "Tạo mới" và "Thay đổi thông tin".')),
    ]

    return [
        ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
        ('II', 'BỘ LỌC & TÌM KIẾM', S2),
        ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
        ('IV', 'THÊM MỚI — CHỌN ' + O.upper() + ' & HỢP ĐỒNG', S4),
        ('V', 'XEM CHI TIẾT, SỬA & LỊCH SỬ', S5),
        ('VI', 'XÓA', S6),
        ('VII', 'IMPORT EXCEL', S7),
        ('VIII', 'XUẤT EXCEL / IN', S8),
        ('IX', 'RÀNG BUỘC NHẬP LIỆU', S9),
        ('X', 'CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI', S10),
        ('XI', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S11),
    ]


for cfg in (KH, NCC):
    print('=' * 20, cfg['title'])
    build(output_file=os.path.join(BASE, cfg['file']),
          sheet_name='Trang tính1',
          feature_name=cfg['title'],
          module_name=cfg['module'],
          description_block=description(cfg),
          role_tcs=role_tcs(cfg),
          sections=sections(cfg))
