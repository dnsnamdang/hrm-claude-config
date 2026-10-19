# -*- coding: utf-8 -*-
"""HDSD dang KICH BAN NGHIEM THU thong luong (khong phai HDSD giao dien) cho 2 bao cao cong no KH,
doi chieu cheo ERP - HRM (user chot 19/10/2026).

Sinh:  HDSD kich ban nghiem thu - BC chi tiet cong no KH.docx
       HDSD kich ban nghiem thu - BC tong hop cong no KH theo nhan vien.docx
Chay:  python ve_so_do.py && python gen_kich_ban.py
Khung: hrm-claude-config/erp/.plans/_hdsd_van_xuoi/hdsd_van_xuoi.py (mau van xuoi + bang, Times New Roman 13).

Nguon noi dung: FE hrm-client/pages/sale/customer-debt-{details,by-employee}/index.vue (nhan, chu thich cot),
BE hrm-api/Modules/Finance/Services/CustomerDebt/* (muc "Giu y ERP" / "Khac ERP"), spec
docs/superpowers/specs/gop-db/2026-10-06-sale-customer-debt-reports-design.md, TC ERP 08/10
(erp/.plans/erp-bao-cao-cong-no-khach-hang/common.py: chuoi phieu + so tien mau).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))  # hrm-claude-config
sys.path.insert(0, os.path.join(ROOT, 'erp', '.plans', '_hdsd_van_xuoi'))
from hdsd_van_xuoi import HdsdVanXuoi, cap_nhat_truong  # noqa: E402

NGAY = '19/10/2026'
SO_DO = os.path.join(HERE, 'so_do_luong.png')
O = '☐ Đạt   ☐ Không đạt'

# ----------------------------------------------------------------------------------------------- đường vào
TC = 'HRM, phân hệ Tài chính'
M = {
    'hd_erp': 'ERP: Kinh doanh › Hợp đồng bán hàng (HRM chưa có màn danh sách hợp đồng bán hàng)',
    'ycxh': TC + ' › Xuất hàng › "Yêu cầu xuất hàng" (hoặc Bán hàng › Yêu cầu › Hàng hóa › "YC xuất hàng")',
    'dnxk': TC + ' › Xuất hàng › "Đề nghị xuất kho"',
    'pxk': 'ERP: Phiếu xuất kho (mục "Phiếu xuất kho" trên HRM mở thẳng sang ERP)',
    'pxh': TC + ' › Xuất hàng › "Phiếu xuất hàng"',
    'dntt': TC + ' › Khởi tạo › "Đề nghị thu tiền"',
    'pt': TC + ' › Quản lý tiền › "Phiếu thu"',
    'pbc': TC + ' › Quản lý tiền › "Phiếu báo có"',
    'ycdc': TC + ' › Khởi tạo › "Phiếu yêu cầu điều chỉnh công nợ"',
    'pkt': TC + ' › Sổ tổng hợp › "Phiếu kế toán"',
    'ycnh': TC + ' › Nhập hàng › "Yêu cầu nhập hàng"',
    'dnnk': TC + ' › Nhập hàng › "Đề nghị nhập kho"',
    'pnk': TC + ' › Nhập hàng › "Phiếu nhập kho"',
    'pnh': TC + ' › Nhập hàng › "Phiếu nhập hàng"',
    'dnthanhtoan': TC + ' › Khởi tạo › "Đề nghị thanh toán"',
    'pc': TC + ' › Quản lý tiền › "Phiếu chi"',
    'unc': TC + ' › Quản lý tiền › "Phiếu ủy nhiệm chi"',
    'so_ct': 'ERP: Kế toán › Khách hàng › "Sổ chi tiết công nợ phải thu khách hàng"',
}

# ----------------------------------------------------------------------------------------------- 2 màn
MAN = {
    'detail': {
        'ten': 'Báo cáo chi tiết công nợ khách hàng',
        'ngan': 'Báo cáo chi tiết công nợ KH',
        'erp': 'Kinh doanh › Báo cáo công nợ › "Báo cáo chi tiết công nợ KH"',
        'hrm': 'phân hệ Bán hàng › Báo cáo › Báo cáo công nợ › "Chi tiết công nợ KH"',
        'nhom': 'khách hàng',
        'dong_nhom': 'dòng khách hàng "KH-TEST - <tên>" (chữ đậm)',
        'cho_xem': 'dòng hợp đồng HD-TEST-01, dòng khách hàng KH-TEST (chữ đậm phía trên) và dòng Tổng cộng',
        'quyen': 'Xem báo cáo chi tiết công nợ khách hàng theo ',
        'file': 'HDSD kich ban nghiem thu - BC chi tiet cong no KH.docx',
        'muc_dich': ('Báo cáo cho biết mỗi KHÁCH HÀNG đang nợ bao nhiêu, tách theo từng hợp đồng: số dư đầu kỳ, '
                     'phát sinh tăng / giảm trong kỳ, số dư cuối kỳ. Mỗi ô số tiền bấm được để xem danh sách phiếu '
                     'tạo ra con số đó. Dùng để kế toán và trưởng bộ phận theo dõi công nợ phải thu.'),
    },
    'employee': {
        'ten': 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên',
        'ngan': 'Báo cáo tổng hợp công nợ KH theo nhân viên',
        'erp': 'Kinh doanh › Báo cáo công nợ › "Báo cáo tổng hợp công nợ khách hàng theo nhân viên"',
        'hrm': 'phân hệ Bán hàng › Báo cáo › Báo cáo công nợ › "Tổng hợp công nợ theo NV"',
        'nhom': 'nhân viên',
        'dong_nhom': 'dòng nhân viên "<mã> - <họ tên nhân viên A>" (chữ đậm)',
        'cho_xem': 'dòng hợp đồng HD-TEST-01, dòng nhân viên A (chữ đậm phía trên) và dòng Tổng cộng',
        'quyen': 'Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên - ',
        'file': 'HDSD kich ban nghiem thu - BC tong hop cong no KH theo nhan vien.docx',
        'muc_dich': ('Báo cáo gom công nợ theo NHÂN VIÊN LẬP HỢP ĐỒNG: mỗi nhân viên có những hợp đồng nào còn '
                     'nợ, nợ bao nhiêu, nghiệm thu ngày nào, khách đã nợ bao nhiêu ngày. Dùng để giao nhân viên '
                     'kinh doanh đi thu nợ.'),
    },
}


def loc(man):
    """Cách lọc khi kiểm (cả 2 hệ thống)."""
    return ('ERP: Từ ngày = ngày 1 tháng này, Đến ngày = hôm nay, Khách hàng = KH-TEST, bấm Lọc. '
            'HRM: ô Thời gian = ngày 1 tháng này đến hôm nay, Khách hàng = KH-TEST (bảng tự tải lại; '
            'muốn chắc thì bấm Tìm kiếm).')


# ================================================================================================= khối chung
def tong_quan(d, man, k):
    d.h1('TỔNG QUAN')
    d.h2('1. Mục đích tài liệu')
    d.p('Tài liệu này là KỊCH BẢN NGHIỆM THU chạy một mạch từ đầu đến cuối cho màn ' + man['ten'] + '. '
        'Người test không cần biết giao diện chi tiết: chỉ cần làm đúng từng bước nghiệp vụ (lập phiếu, duyệt, hạch '
        'toán), sau mỗi bước mở báo cáo trên CẢ HAI hệ thống ERP và HRM, rồi so con số với kết quả mong đợi.')
    d.p('Mỗi kịch bản có mã NT-xx, mục tiêu, điều kiện trước, các bước, kết quả mong đợi và ô ghi kết quả. Cuối tài '
        'liệu có biên bản tổng hợp để ký nghiệm thu.')
    d.h2('2. Lịch sử cập nhật tài liệu')
    d.table([['Phiên bản', 'Ngày', 'Nội dung', 'Người thực hiện'],
             ['1.0', NGAY, 'Khởi tạo kịch bản nghiệm thu thông luồng, đối chiếu chéo ERP - HRM', 'Phòng Phát triển']],
            widths=[0.9, 1.1, 3.0, 1.5])
    d.h2('3. Báo cáo dùng để làm gì')
    d.p(man['muc_dich'])
    d.bullet('Trên ERP: ', 'menu ' + man['erp'] + '.')
    d.bullet('Trên HRM: ', man['hrm'] + '.')
    d.h2('4. Nguyên tắc nghiệm thu')
    d.bullet('Lập phiếu một lần, kiểm hai nơi: ', 'ERP và HRM ở môi trường test dùng chung một kho dữ liệu, nên '
             'phiếu lập ở hệ thống nào cũng lên báo cáo của cả hai. Khuyến nghị lập ở HRM với các màn đã chuyển '
             'sang (để nghiệm thu luôn luồng HRM); hợp đồng bán hàng và phiếu xuất kho vẫn lập ở ERP.')
    d.bullet('ERP là số chuẩn: ', 'HRM phải ra ĐÚNG con số như ERP ở mọi ô, trừ các điểm khác nhau đã chốt ở PHẦN 5.')
    d.bullet('Chỉ phiếu đã hạch toán mới lên báo cáo: ', 'phiếu mới lập, đang chờ duyệt, chưa hạch toán thì báo cáo '
             'chưa đổi. Báo cáo lọc theo NGÀY HẠCH TOÁN, không theo ngày lập phiếu.')
    d.bullet('So chênh lệch, không so số tuyệt đối: ', 'trước mỗi bước ghi lại "số nền"; kết quả đúng là phần chênh '
             'so với số nền.')
    d.h2('5. Thuật ngữ')
    d.table([['Thuật ngữ', 'Ý nghĩa'],
             ['Hạch toán', 'Kế toán ghi nhận phiếu vào sổ công nợ. Chỉ phiếu đã hạch toán mới lên báo cáo.'],
             ['Số dư đầu kỳ', 'Công nợ cộng dồn từ mọi phiếu có ngày hạch toán TRƯỚC Từ ngày.'],
             ['Phát sinh tăng', 'Hàng hóa/Dịch vụ (xuất bán, hạch toán dịch vụ…) + Điều chỉnh công nợ ghi tăng.'],
             ['Phát sinh giảm', 'Nhập trả lại + Đã thanh toán (phiếu thu, báo có) + Điều chỉnh công nợ ghi giảm.'],
             ['Trả lại tiền thừa', 'Phiếu chi, phiếu ủy nhiệm chi trả tiền lại cho khách; làm số dư TĂNG.'],
             ['Số dư cuối kỳ', 'Đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa. Dương = Dư nợ, âm = Dư có.'],
             ['Số nền', 'Số liệu chụp lại ngay trước một bước, dùng để tính chênh lệch sau bước đó.'],
             ['Đạt / Không đạt', 'Đạt: cả ERP và HRM ra đúng kết quả mong đợi (hoặc lệch đúng điểm đã chốt ở PHẦN 5).']]
            + ([['Ngày nghiệm thu', 'Mốc tính tuổi nợ của hợp đồng (cách xác định ở NT-15).'],
                ['Số ngày nợ', 'Hôm nay - (Ngày nghiệm thu + 6 ngày); âm thì ghi 0; chỉ hiện khi hợp đồng còn dư nợ.']]
               if k == 'employee' else []),
            widths=[1.8, 4.7])
    d.h2('6. Sơ đồ luồng nghiệm thu')
    d.image(SO_DO, 'Luồng nghiệm thu: lập phiếu một lần, kiểm số trên cả ERP và HRM')
    d.h2('7. Bảng phiếu nào làm đổi cột nào')
    d.table([['Cột trên báo cáo', 'Thay đổi khi hạch toán', 'Hướng số dư'],
             ['Hàng hóa/Dịch vụ', 'Phiếu xuất hàng bán theo hợp đồng, phiếu xuất bán hàng mượn, phiếu hạch toán dịch vụ, biên bản thanh lý, khai báo công nợ đầu kỳ', 'Tăng'],
             ['Điều chỉnh công nợ (tăng)', 'Phiếu kế toán từ yêu cầu điều chỉnh công nợ loại TĂNG', 'Tăng'],
             ['Nhập trả lại', 'Phiếu nhập hàng khách trả lại theo hợp đồng', 'Giảm'],
             ['Đã thanh toán', 'Phiếu thu, phiếu báo có, khai báo công nợ đầu kỳ (phần đã thu)', 'Giảm'],
             ['Điều chỉnh công nợ (giảm)', 'Phiếu kế toán từ yêu cầu điều chỉnh công nợ loại GIẢM', 'Giảm'],
             ['Trả lại tiền thừa', 'Phiếu chi, phiếu ủy nhiệm chi trả tiền cho khách', 'Tăng']],
            widths=[1.8, 3.6, 1.1])


def chuan_bi(d, man, k):
    d.h1('PHẦN 1: CHUẨN BỊ TRƯỚC KHI NGHIỆM THU')
    d.h2('1.1. Tài khoản và quyền')
    d.p('Quyền xem báo cáo ở ERP và HRM được cấp RIÊNG ở mỗi hệ thống (tên quyền giống nhau). Thiếu quyền ở một bên '
        'thì hai bên sẽ ra phạm vi dữ liệu khác nhau và kết quả so sánh sai.')
    d.table([['Vai trò', 'Dùng để', 'Quyền cần có (cấp ở CẢ ERP và HRM)'],
             ['Nhân viên A (kinh doanh)', 'Lập hợp đồng HD-TEST-01, lập yêu cầu xuất / nhập hàng, đề nghị thu tiền', 'Không cần quyền xem báo cáo'],
             ['Kế toán', 'Duyệt, lập và hạch toán phiếu xuất hàng, phiếu thu, báo có, phiếu kế toán, phiếu nhập hàng, phiếu chi, ủy nhiệm chi', 'Quyền lập / duyệt / hạch toán các phiếu tương ứng'],
             ['Kho', 'Lập phiếu xuất kho, phiếu nhập kho', 'Quyền kho'],
             ['Người nghiệm thu (Q)', 'Mở báo cáo, so số ERP - HRM', '"' + man['quyen'] + 'tổng công ty"']],
            widths=[1.6, 2.9, 2.0])
    d.h2('1.2. Dữ liệu mẫu')
    d.table([['Dữ liệu', 'Giá trị mẫu', 'Ghi chú'],
             ['Khách hàng', 'KH-TEST', 'Khách hàng tạo riêng cho đợt test, chưa có phát sinh.'],
             ['Hợp đồng bán hàng', 'HD-TEST-01', 'Nhân viên A lập trên ERP, menu Kinh doanh › Hợp đồng bán hàng (HRM chưa có màn này); đã ký; hàng KHÔNG cần lắp đặt.'],
             ['Hợp đồng thứ hai', 'HD-TEST-02', 'Cùng khách KH-TEST, nhân viên A lập; dùng ở NT-14.'],
             ['Kỳ lọc', 'Ngày 1 tháng hiện tại đến hôm nay', 'Mọi phiếu hạch toán trong kỳ này, trừ khi kịch bản nói khác.'],
             ['Số tiền mẫu', 'Xem từng kịch bản', 'Chọn số "tròn" để dễ cộng trừ; có thể đổi nhưng phải tính lại kết quả mong đợi.']],
            widths=[1.6, 1.9, 3.0])
    d.h2('1.3. Cách lọc báo cáo khi kiểm')
    d.p(loc(man))
    d.p('Chỗ quan sát sau mỗi bước: ' + man['cho_xem'] + '.')
    d.h2('1.4. Mẫu ghi số nền')
    d.p('Chép bảng dưới ra giấy / Excel, mỗi bước một dòng. Chỉ cần ghi các cột có thay đổi.')
    d.table([['Bước', 'Cột', 'Số trên ERP', 'Số trên HRM', 'Chênh so với bước trước', 'Khớp?'],
             ['NT-01', 'Số dư cuối kỳ', '', '', '(số nền)', ''],
             ['NT-02', 'Hàng hóa/Dịch vụ', '', '', '+10,000,000', ''],
             ['…', '', '', '', '', '']],
            widths=[0.7, 1.4, 1.1, 1.1, 1.4, 0.8])


def kb(d, ma, ten, muc_tieu, dieu_kien, buoc, ket_qua, khac=None):
    """Một kịch bản: heading + mục tiêu + điều kiện + bảng bước + kết quả mong đợi + ô ghi kết quả."""
    d.h2(ma + '. ' + ten)
    d.note('Mục tiêu: ', muc_tieu)
    d.note('Điều kiện trước: ', dieu_kien)
    rows = [['Bước', 'Ai / Ở đâu', 'Thao tác']]
    for i, (ai, viec) in enumerate(buoc, 1):
        rows.append([str(i), ai, viec])
    d.table(rows, widths=[0.6, 1.7, 4.2])
    d.note('Kết quả mong đợi (ERP và HRM):', '')
    for x in ket_qua:
        d.bullet(x)
    if khac:
        d.note('Khác nhau ERP - HRM được chấp nhận: ', khac)
    d.note('Kết quả: ', 'ERP ' + O + '      HRM ' + O)


def luong_chinh(d, man, k):
    w = man['cho_xem']
    nhom = man['nhom']
    d.h1('PHẦN 2: KỊCH BẢN LUỒNG CHÍNH (TỪ ĐẦU ĐẾN CUỐI)')
    d.p('Làm theo đúng thứ tự NT-01 đến NT-13. Mỗi kịch bản dùng kết quả của kịch bản trước làm số nền.')

    kb(d, 'NT-01', 'Ghi số nền và so khớp ban đầu',
       'Chứng minh trước khi lập phiếu, ERP và HRM đã ra cùng số liệu cho KH-TEST.',
       'Đã có KH-TEST, HD-TEST-01; người nghiệm thu Q có quyền tổng công ty ở cả hai hệ thống.',
       [('Q - ERP', 'Mở ' + man['ngan'] + ', lọc như mục 1.3, ghi lại 8 cột số của ' + w + '.'),
        ('Q - HRM', 'Mở cùng báo cáo trên HRM, lọc cùng kỳ, cùng khách, ghi lại cùng các dòng.'),
        ('Q - ERP', 'Mở ' + M['so_ct'] + ', cùng khách, cùng kỳ, ghi Số dư cuối kỳ.')],
       ['Mọi ô số của ERP và HRM bằng nhau (khách mới thì toàn bộ trống / bằng 0).',
        'Số dư cuối kỳ của dòng Tổng cộng bằng số dư trên sổ chi tiết công nợ phải thu.',
        'Có đủ số liệu làm số nền cho NT-02.'])

    kb(d, 'NT-02', 'Xuất bán hàng làm tăng công nợ (10,000,000)',
       'Đi hết luồng xuất bán: chỉ khi phiếu xuất hàng được hạch toán thì báo cáo mới tăng.',
       'Đã có số nền NT-01.',
       [('Nhân viên A - HRM', 'Vào ' + M['ycxh'] + ', lập yêu cầu xuất hàng cho HD-TEST-01, giá trị 10,000,000, gửi duyệt và duyệt xong.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo. Ghi nhận: CHƯA thay đổi.'),
        ('Kế toán kho - HRM', 'Vào ' + M['dnxk'] + ', lập đề nghị xuất kho từ yêu cầu trên, duyệt.'),
        ('Kho - ERP', 'Lập và duyệt phiếu xuất kho (' + M['pxk'] + ').'),
        ('Kế toán - HRM', 'Vào ' + M['pxh'] + ', lập phiếu xuất hàng cho lần xuất kho trên, hạch toán ngày hôm nay.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo, so với số nền.')],
       ['Bước 2: không cột nào thay đổi (yêu cầu xuất hàng chưa ghi công nợ).',
        'Bước 6: cột Hàng hóa/Dịch vụ +10,000,000; Cộng (phát sinh tăng) +10,000,000; Số dư cuối kỳ +10,000,000 ở ' + w + '.',
        'ERP và HRM ra cùng số.'] +
       (['HRM: bấm vào số 10,000,000 ở cột Hàng hóa/Dịch vụ của HD-TEST-01: cửa sổ "Chi tiết chứng từ" liệt kê đúng 1 phiếu xuất hàng vừa lập, số tiền 10,000,000.',
         'ERP: bấm cùng ô, cửa sổ chi tiết cũng có đúng phiếu xuất hàng đó.']
        if k == 'detail' else
        ['Cột Ngày nghiệm thu của HD-TEST-01 = ngày duyệt phiếu xuất kho (hôm nay); Số ngày nợ = 0 (chưa quá 6 ngày).']),
       'ERP hiện tiêu đề cửa sổ chi tiết luôn là "Chi tiết số tiền đã thanh toán"; HRM hiện "Chi tiết chứng từ" kèm tên cột và số hợp đồng.'
       if k == 'detail' else None)

    kb(d, 'NT-03', 'Phiếu chưa hoàn tất không làm đổi số',
       'Phiếu chưa duyệt / chưa hạch toán không được lên báo cáo.',
       'Số nền = kết quả NT-02.',
       [('Nhân viên A - HRM', 'Lập thêm một yêu cầu xuất hàng 5,000,000 cho HD-TEST-01, CHƯA đề nghị xuất kho.'),
        ('Kế toán - HRM', 'Lập một phiếu thu 1,000,000 cho HD-TEST-01, để ở trạng thái chưa duyệt / chưa hạch toán.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo.')],
       ['Không cột nào thay đổi so với số nền, ở cả ERP và HRM.',
        'Xóa (hoặc hủy) 2 phiếu nháp này trước khi sang NT-04 để không lẫn số.'])

    kb(d, 'NT-04', 'Khách trả tiền bằng phiếu thu (4,000,000)',
       'Phiếu thu đã hạch toán làm tăng cột Đã thanh toán, giảm số dư.',
       'Số nền = kết quả NT-02.',
       [('Nhân viên A - HRM', 'Vào ' + M['dntt'] + ', lập đề nghị thu tiền của KH-TEST cho HD-TEST-01, 4,000,000, gửi duyệt.'),
        ('Kế toán - HRM', 'Vào ' + M['pt'] + ', lập phiếu thu từ đề nghị trên (hoặc lập thẳng), chọn KH-TEST và HD-TEST-01, duyệt và hạch toán hôm nay.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo.')],
       ['Cột Đã thanh toán +4,000,000; Cộng (phát sinh giảm) +4,000,000; Số dư cuối kỳ -4,000,000 ở ' + w + '.'] +
       (['Bấm ô Đã thanh toán của HD-TEST-01: cửa sổ chi tiết có mã phiếu thu vừa lập, 4,000,000.'] if k == 'detail' else []))

    kb(d, 'NT-05', 'Khách chuyển khoản - phiếu báo có (1,000,000)',
       'Phiếu báo có cũng tính vào cột Đã thanh toán.',
       'Số nền = kết quả NT-04.',
       [('Kế toán - HRM', 'Vào ' + M['pbc'] + ', lập phiếu báo có của KH-TEST cho HD-TEST-01, 1,000,000, hạch toán hôm nay.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo.')],
       ['Cột Đã thanh toán +1,000,000 (lũy kế 5,000,000); Số dư cuối kỳ -1,000,000.'])

    kb(d, 'NT-06', 'Điều chỉnh công nợ TĂNG (2,000,000)',
       'Phiếu kế toán điều chỉnh tăng đi vào nhóm Phát sinh tăng.',
       'Số nền = kết quả NT-05.',
       [('Nhân viên A - HRM', 'Vào ' + M['ycdc'] + ', lập yêu cầu điều chỉnh TĂNG công nợ KH-TEST, hợp đồng HD-TEST-01, 2,000,000, gửi duyệt.'),
        ('Người duyệt - HRM', 'Duyệt yêu cầu (mục Chờ duyệt của phân hệ Tài chính).'),
        ('Kế toán - HRM', 'Vào ' + M['pkt'] + ', lập phiếu kế toán từ yêu cầu trên, hạch toán hôm nay.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo.')],
       ['Cột Điều chỉnh công nợ thuộc nhóm Phát sinh TĂNG +2,000,000; Cộng (phát sinh tăng) +2,000,000; Số dư cuối kỳ +2,000,000.',
        'Sau bước 2 (mới duyệt, chưa có phiếu kế toán): báo cáo chưa đổi.'])

    kb(d, 'NT-07', 'Điều chỉnh công nợ GIẢM (500,000)',
       'Phiếu kế toán điều chỉnh giảm đi vào nhóm Phát sinh giảm.',
       'Số nền = kết quả NT-06.',
       [('Nhân viên A, người duyệt, kế toán - HRM', 'Làm như NT-06 nhưng chọn loại điều chỉnh GIẢM, 500,000.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo.')],
       ['Cột Điều chỉnh công nợ thuộc nhóm Phát sinh GIẢM +500,000; Cộng (phát sinh giảm) +500,000; Số dư cuối kỳ -500,000.'])

    kb(d, 'NT-08', 'Khách trả lại hàng (3,000,000)',
       'Đi hết luồng nhập hàng trả lại; chỉ phiếu nhập hàng đã hạch toán mới làm tăng cột Nhập trả lại.',
       'HD-TEST-01 đã xuất hàng ở NT-02. Số nền = kết quả NT-07.',
       [('Nhân viên A - HRM', 'Vào ' + M['ycnh'] + ', lập yêu cầu nhập hàng khách trả lại theo HD-TEST-01, giá trị 3,000,000, duyệt.'),
        ('Kế toán kho - HRM', 'Vào ' + M['dnnk'] + ', lập đề nghị nhập kho, duyệt.'),
        ('Kho - HRM', 'Vào ' + M['pnk'] + ', lập và duyệt phiếu nhập kho.'),
        ('Kế toán - HRM', 'Vào ' + M['pnh'] + ', lập phiếu nhập hàng, hạch toán hôm nay.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo.')],
       ['Cột Nhập trả lại +3,000,000; Cộng (phát sinh giảm) +3,000,000; Số dư cuối kỳ -3,000,000.',
        'Trước bước 4 báo cáo chưa đổi.'])

    kb(d, 'NT-09', 'Trả lại tiền thừa bằng phiếu chi (200,000)',
       'Phiếu chi trả tiền cho khách làm cột Trả lại tiền thừa tăng và số dư TĂNG.',
       'Số nền = kết quả NT-08.',
       [('Nhân viên A - HRM', 'Vào ' + M['dnthanhtoan'] + ', lập đề nghị thanh toán trả KH-TEST cho HD-TEST-01, 200,000, duyệt.'),
        ('Kế toán - HRM', 'Vào ' + M['pc'] + ', lập phiếu chi, hạch toán hôm nay.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo.')],
       ['Cột Trả lại tiền thừa +200,000; Số dư cuối kỳ TĂNG 200,000.'])

    kb(d, 'NT-10', 'Trả lại tiền thừa bằng ủy nhiệm chi (300,000)',
       'Phiếu ủy nhiệm chi cũng vào cột Trả lại tiền thừa.',
       'Số nền = kết quả NT-09.',
       [('Kế toán - HRM', 'Vào ' + M['unc'] + ', lập ủy nhiệm chi trả KH-TEST cho HD-TEST-01, 300,000, hạch toán hôm nay.'),
        ('Q - ERP + HRM', 'Lọc lại báo cáo.')],
       ['Cột Trả lại tiền thừa +300,000 (lũy kế 500,000); Số dư cuối kỳ TĂNG 300,000.'])

    d.h2('NT-11. Kiểm tổng sau cả chuỗi phiếu')
    d.note('Mục tiêu: ', 'Chứng minh báo cáo cộng đúng toàn bộ luồng, và ERP - HRM khớp nhau ở mọi dòng.')
    d.p('So Số dư cuối kỳ của HD-TEST-01 với số nền NT-01. Chênh lệch đúng:')
    d.p([('+10,000,000 - 4,000,000 - 1,000,000 + 2,000,000 - 500,000 - 3,000,000 + 200,000 + 300,000 = +4,000,000', 'b')])
    d.table([['Cột', 'Chênh so với NT-01', 'ERP', 'HRM'],
             ['Hàng hóa/Dịch vụ', '+10,000,000', '', ''],
             ['Điều chỉnh công nợ (tăng)', '+2,000,000', '', ''],
             ['Cộng (phát sinh tăng)', '+12,000,000', '', ''],
             ['Nhập trả lại', '+3,000,000', '', ''],
             ['Đã thanh toán', '+5,000,000', '', ''],
             ['Điều chỉnh công nợ (giảm)', '+500,000', '', ''],
             ['Cộng (phát sinh giảm)', '+8,500,000', '', ''],
             ['Trả lại tiền thừa', '+500,000', '', ''],
             ['Số dư cuối kỳ', '+4,000,000', '', '']],
            widths=[2.3, 1.8, 1.2, 1.2])
    d.bullet('Dòng hợp đồng HD-TEST-01, ' + man['dong_nhom'] + ' và dòng Tổng cộng đều chênh đúng như bảng.')
    d.bullet('ERP và HRM bằng nhau ở mọi ô.')
    d.note('Kết quả: ', 'ERP ' + O + '      HRM ' + O)

    kb(d, 'NT-12', 'Thu vượt - hợp đồng chuyển sang Dư có, kiểm bộ lọc Số dư cuối kỳ',
       'Số dư âm hiện đúng và lọc Dư nợ / Dư có đúng.',
       'HD-TEST-01 đang dư nợ 4,000,000 (nếu số nền NT-01 bằng 0).',
       [('Kế toán - HRM', 'Lập phiếu thu 5,000,000 cho HD-TEST-01, hạch toán hôm nay.'),
        ('Q - ERP + HRM', 'Lọc lại, Số dư cuối kỳ = Tất cả.'),
        ('Q - ERP + HRM', 'Đổi Số dư cuối kỳ = Dư nợ.'),
        ('Q - ERP + HRM', 'Đổi Số dư cuối kỳ = Dư có.')],
       ['Bước 2: Số dư cuối kỳ của HD-TEST-01 = -1,000,000.',
        'Bước 3: HD-TEST-01 không còn trong bảng.',
        'Bước 4: HD-TEST-01 có trong bảng.',
        'Dòng Tổng cộng KHÔNG đổi giữa bước 2, 3, 4 (bộ lọc Dư nợ / Dư có không áp cho dòng Tổng cộng) - đúng ở cả hai hệ thống.'])

    kb(d, 'NT-13', 'Ngày hạch toán quyết định kỳ - hủy phiếu thì số trả về',
       'Phiếu trước Từ ngày vào Số dư đầu kỳ; sau Đến ngày không tính; hủy hạch toán thì báo cáo trả lại như cũ.',
       'Một phiếu thu 700,000 của KH-TEST cho HD-TEST-01, ngày hạch toán là ngày cuối tháng trước.',
       [('Q - ERP + HRM', 'Lọc kỳ tháng này (ngày 1 đến hôm nay).'),
        ('Q - ERP + HRM', 'Đổi Từ ngày về ngày 1 tháng trước, lọc lại.'),
        ('Q - ERP + HRM', 'Lọc Đến ngày = hôm qua (Từ ngày = ngày 1 tháng này).'),
        ('Kế toán - HRM', 'Hủy hạch toán (hoặc xóa) phiếu thu 5,000,000 ở NT-12.'),
        ('Q - ERP + HRM', 'Lọc lại kỳ tháng này.')],
       ['Bước 1: phiếu 700,000 KHÔNG nằm ở cột Đã thanh toán mà làm Số dư đầu kỳ giảm 700,000.',
        'Bước 2: phiếu chuyển sang cột Đã thanh toán; Số dư cuối kỳ KHÔNG đổi so với bước 1.',
        'Bước 3: các phiếu hạch toán hôm nay (NT-02 đến NT-12) không được tính.',
        'Bước 5: cột Đã thanh toán giảm lại 5,000,000; Số dư cuối kỳ tăng lại 5,000,000.'])


# ================================================================================================= riêng từng màn
def rieng_chi_tiet(d):
    d.h1('PHẦN 3: KỊCH BẢN RIÊNG CỦA MÀN CHI TIẾT')
    kb(d, 'NT-14', 'Dòng khách hàng cộng đủ mọi hợp đồng',
       'Dòng khách hàng là tổng của tất cả hợp đồng của khách, kể cả hợp đồng nằm ở trang sau.',
       'KH-TEST có HD-TEST-01 (sau NT-13) và HD-TEST-02.',
       [('Kế toán - HRM', 'Xuất hàng cho HD-TEST-02 giá trị 6,000,000 theo luồng NT-02, hạch toán hôm nay.'),
        ('Q - ERP + HRM', 'Lọc kỳ tháng này, Khách hàng = KH-TEST.'),
        ('Q - HRM', 'Chọn Số dòng/trang = 10, lọc bỏ ô Khách hàng (xem mọi khách), tìm trang có KH-TEST.')],
       ['Bước 2: dòng KH-TEST = HD-TEST-01 + HD-TEST-02 ở từng cột; cột Hàng hóa/Dịch vụ của dòng khách tăng 6,000,000.',
        'Mỗi dòng hợp đồng hiện đúng Phòng ban, Bộ phận, NVKD của nhân viên A (theo hồ sơ hiện tại).',
        'Bước 3 (HRM): nếu 2 hợp đồng rơi vào 2 trang, cả 2 trang đều hiện CÙNG một tổng dòng KH-TEST.'],
       'ERP chỉ cộng các hợp đồng nằm trên trang đang xem, nên khi khách vắt qua 2 trang thì dòng khách của ERP nhỏ hơn HRM. Lọc riêng KH-TEST (bước 2) thì hai bên phải bằng nhau.')

    kb(d, 'NT-15', 'Cửa sổ chứng từ khớp với ô số tiền',
       'Mỗi ô số tiền mở ra đúng các phiếu đã lập ở PHẦN 2, cộng lại bằng ô.',
       'Đã chạy NT-02 đến NT-10; lọc kỳ tháng này, Khách hàng = KH-TEST.',
       [('Q - HRM', 'Bấm lần lượt ô Hàng hóa/Dịch vụ, Điều chỉnh công nợ (tăng), Nhập trả lại, Đã thanh toán, Điều chỉnh công nợ (giảm), Trả lại tiền thừa của HD-TEST-01.'),
        ('Q - HRM', 'Bấm các ô tương ứng ở dòng khách hàng KH-TEST.'),
        ('Q - ERP', 'Bấm cùng các ô trên ERP.')],
       ['Mỗi cửa sổ liệt kê đúng mã các phiếu đã lập ở PHẦN 2 cho cột đó, tổng tiền trong cửa sổ bằng số trên ô.',
        'Cửa sổ của dòng khách hàng gồm phiếu của cả HD-TEST-01 và HD-TEST-02.',
        'Danh sách mã phiếu của ERP và HRM giống nhau.',
        'HRM: ô bằng 0 để trống và không bấm được.'],
       'ERP hiện dấu "-" ở ô bằng 0 và vẫn bấm được (có thể ra phiếu, ví dụ cột Điều chỉnh công nợ giảm vẫn liệt kê phiếu thu). HRM bỏ link ở ô 0 theo chốt 07/10/2026. Cửa sổ của cột Điều chỉnh công nợ ở cả hai hệ thống có thể liệt kê thêm phiếu thu / khai báo đầu kỳ - giữ như ERP.')

    kb(d, 'NT-16', 'Hợp đồng lập bên HRM và khách hàng không còn trong danh mục',
       'Các trường hợp ERP hiển thị sai, HRM đã sửa.',
       'Có một hợp đồng dự án lập trên HRM (Bán hàng › Hợp đồng bán hàng › "Hợp đồng (dự án TKT)") đã có phiếu thu hạch toán.',
       [('Q - ERP + HRM', 'Lọc kỳ có phiếu đó, Khách hàng = khách của hợp đồng.')],
       ['HRM: cột Đơn hàng/hợp đồng hiện mã hợp đồng, bấm mở được hợp đồng.',
        'ERP: hiện dấu "-" (lỗi ERP đã biết, ghi vào cột Ghi chú, KHÔNG tính là lỗi HRM).',
        'Các cột số tiền của dòng đó bằng nhau ở hai hệ thống.'])


def rieng_theo_nv(d):
    d.h1('PHẦN 3: KỊCH BẢN RIÊNG CỦA MÀN THEO NHÂN VIÊN')
    kb(d, 'NT-14', 'Gom theo nhân viên LẬP hợp đồng, dòng nhân viên cộng đủ',
       'Hợp đồng nằm dưới đúng người lập; dòng nhân viên là tổng của tất cả hợp đồng của họ.',
       'Nhân viên A lập HD-TEST-01 và HD-TEST-02. Khách KH-TEST đang do nhân viên khác phụ trách (nếu có thể).',
       [('Kế toán - HRM', 'Xuất hàng cho HD-TEST-02 giá trị 6,000,000 theo luồng NT-02, hạch toán hôm nay.'),
        ('Q - ERP + HRM', 'Lọc kỳ tháng này, Khách hàng = KH-TEST.'),
        ('Q - HRM', 'Chọn Số dòng/trang = 10, bỏ ô Khách hàng, tìm trang có nhân viên A.')],
       ['Bước 2: HD-TEST-01, HD-TEST-02 nằm dưới dòng nhân viên A (người lập), không nằm dưới người phụ trách khách hàng.',
        'Dòng nhân viên A = HD-TEST-01 + HD-TEST-02 ở từng cột; cột Khách hàng của 2 dòng hợp đồng = "KH-TEST - <tên>".',
        'Bước 3 (HRM): nếu hợp đồng của A rơi vào 2 trang, cả 2 trang đều hiện CÙNG một tổng dòng nhân viên A.'],
       'ERP chỉ cộng hợp đồng trên trang đang xem, nên nhân viên vắt qua 2 trang thì dòng nhân viên của ERP nhỏ hơn HRM. Lọc riêng KH-TEST hoặc riêng nhân viên A thì hai bên phải bằng nhau.')

    d.h2('NT-15. Ngày nghiệm thu và Số ngày nợ')
    d.note('Mục tiêu: ', 'Ngày nghiệm thu lấy đúng nguồn theo loại hợp đồng; Số ngày nợ tính tới HÔM NAY.')
    d.note('Cách xác định Ngày nghiệm thu: ', '')
    d.table([['Loại hợp đồng', 'Ngày nghiệm thu lấy từ'],
             ['Hợp đồng hãng cần lắp đặt', 'Ngày biên bản nghiệm thu bàn giao mới nhất.'],
             ['Hợp đồng hãng không cần lắp đặt', 'Ngày muộn nhất trong: phiếu xuất kho bán hàng, phiếu xuất bán hàng mượn, phiếu hạch toán dịch vụ.'],
             ['Hợp đồng dịch vụ bảo hành - sửa chữa', 'Ngày muộn nhất trong: hạch toán dịch vụ, phiếu xuất bán hàng mượn, phiếu xuất kho.'],
             ['Không có các phiếu trên', 'Ngày bàn giao nghiệm thu khai ở công nợ đầu kỳ quá hạn; không có thì để trống.']],
            widths=[2.3, 4.2])
    d.table([['Bước', 'Tình huống', 'Cách làm', 'Kết quả đúng (ERP và HRM)'],
             ['1', 'Hợp đồng không cần lắp đặt', 'HD-TEST-01 đã xuất kho ở NT-02 (hôm nay).', 'Ngày nghiệm thu = hôm nay; Số ngày nợ = 0.'],
             ['2', 'Hợp đồng đã nghiệm thu lâu', 'Lọc một hợp đồng có thật, còn nợ, Ngày nghiệm thu cách hôm nay 30 ngày.', 'Số ngày nợ = 30 - 6 = 24.'],
             ['3', 'Hợp đồng cần lắp đặt', 'Một hợp đồng hãng cần lắp đặt đã xuất hàng; lập biên bản nghiệm thu bàn giao ngày 10 của tháng.', 'Ngày nghiệm thu = ngày 10 (theo biên bản, không theo ngày xuất kho).'],
             ['4', 'Hết nợ', 'Lập phiếu thu đủ số còn nợ của một hợp đồng, hạch toán hôm nay.', 'Số dư cuối kỳ = 0 (ô trống); Số ngày nợ để trống; Ngày nghiệm thu vẫn hiện.'],
             ['5', 'Lọc theo Ngày nghiệm thu', 'Chọn đúng ngày nghiệm thu của hợp đồng ở bước 2, rồi chọn ngày hôm sau.', 'Lần 1 có hợp đồng; lần 2 không có (lọc đúng bằng ngày).']],
            widths=[0.65, 1.45, 2.3, 2.1])
    d.note('Khác nhau ERP - HRM được chấp nhận: ', 'Số ngày nợ tính theo giờ hiện tại nên hai lần xem cách nhau qua mốc ngày có thể lệch 1 ngày - mở ERP và HRM liền nhau rồi so. Lọc theo Ngày nghiệm thu chậm ở cả hai hệ thống.')
    d.note('Kết quả: ', 'ERP ' + O + '      HRM ' + O)

    kb(d, 'NT-16', 'Xuất Excel mẫu in',
       'File mẫu in dùng để giao nhân viên ghi giải trình, kế hoạch thu nợ.',
       'Đã chạy PHẦN 2; lọc kỳ tháng này, Khách hàng = KH-TEST.',
       [('Q - HRM', 'Bấm "Xuất Excel mẫu in".'),
        ('Q - ERP', 'Bấm "Xuất Excel Mẫu In", chờ file gửi về email.')],
       ['HRM tải file ngay; ERP gửi file qua email.',
        'Dòng HD-TEST-01 trong 2 file có cùng Giá trị hợp đồng thực tế, Giá trị đã thanh toán, Còn nợ cuối kỳ, Ngày nghiệm thu, Số ngày nợ.',
        'Có các cột trống để nhân viên ghi giải trình, kế hoạch thu hồi, xác nhận công nợ.'])


# ================================================================================================= quyền + đối chiếu
def phan_quyen(d, man, k):
    d.h1('PHẦN 4: PHÂN QUYỀN, ĐỐI CHIẾU CHÉO VÀ XUẤT EXCEL')
    d.h2('NT-17. Phạm vi dữ liệu theo quyền')
    d.note('Mục tiêu: ', 'Mỗi tài khoản chỉ thấy công nợ trong phạm vi quyền; ERP và HRM cho cùng danh sách hợp đồng.')
    d.note('Điều kiện trước: ', 'Cấp quyền GIỐNG NHAU ở cả ERP và HRM cho 5 tài khoản dưới đây. Mỗi tài khoản lọc kỳ tháng này, không lọc khách hàng.')
    them = ' + phòng đang ngồi' if k == 'employee' else ''
    them_bp = ' + bộ phận đang ngồi' if k == 'employee' else ''
    d.table([['Tài khoản', 'Quyền', 'Kết quả đúng (ERP và HRM)'],
             ['A', 'Không có quyền nào', 'Chỉ hợp đồng A lập (có HD-TEST-01, HD-TEST-02). Không có ô Công ty / Phòng ban / Bộ phận / Nhân viên.'],
             ['B', '"' + man['quyen'] + 'bộ phận"', 'Hợp đồng của các bộ phận B được phân quản lý' + them_bp + ' + hợp đồng B lập.'],
             ['C', '"' + man['quyen'] + 'phòng ban"', 'Hợp đồng của các phòng C được phân quản lý' + them + ' + hợp đồng C lập.'],
             ['D', '"' + man['quyen'] + 'công ty"', 'Hợp đồng của công ty D + hợp đồng D lập; không có công ty khác.'],
             ['E', '"' + man['quyen'] + 'tổng công ty"', 'Mọi công ty; có đủ ô Công ty, Phòng ban, Bộ phận, Nhân viên.']],
            widths=[0.8, 2.6, 3.1])
    d.p('Với từng tài khoản: danh sách hợp đồng và 8 cột số của từng hợp đồng phải giống nhau giữa ERP và HRM.')
    if k == 'detail':
        d.note('Khác nhau ERP - HRM được chấp nhận: ', 'với tài khoản A và B, Số dư đầu kỳ của dòng Tổng cộng trên ERP là số '
               'của TOÀN HỆ THỐNG (hàng trăm tỷ) - lỗi bảo mật của ERP; HRM chỉ tính trong phạm vi được xem. Với C, D, E '
               'hai bên phải bằng nhau.')
    else:
        d.note('Khác nhau ERP - HRM được chấp nhận: ', 'Số dư đầu kỳ của dòng Tổng cộng trên ERP luôn là số của TOÀN HỆ '
               'THỐNG với mọi tài khoản - lỗi bảo mật của ERP; HRM chỉ tính trong phạm vi được xem. Chỉ với E (tổng công '
               'ty) hai bên mới bằng nhau ở ô này. Ngoài ra, trên ERP tài khoản A dùng công cụ sửa đường dẫn có thể xem '
               'được hợp đồng của nhân viên khác; HRM luôn chỉ trả hợp đồng của A (dành cho tester kỹ thuật).')
    d.note('Kết quả: ', 'ERP ' + O + '      HRM ' + O)

    d.h2('NT-18. Đối chiếu chéo với các báo cáo công nợ khác')
    d.note('Mục tiêu: ', 'Các báo cáo công nợ đọc chung một sổ nên phải ra cùng số cho cùng khách, cùng kỳ.')
    d.note('Điều kiện trước: ', 'Đã chạy PHẦN 2 và PHẦN 3; người nghiệm thu E (tổng công ty); lọc kỳ tháng này, Khách hàng = KH-TEST.')
    khac = 'Báo cáo tổng hợp công nợ KH theo nhân viên' if k == 'detail' else 'Báo cáo chi tiết công nợ KH'
    d.table([['So với', 'So cái gì', 'Kết quả đúng'],
             [khac + ' (ERP và HRM)', '8 cột số của HD-TEST-01, HD-TEST-02', 'Bằng nhau.'],
             [khac + ' (ERP và HRM)', 'Dòng Tổng cộng', 'Bằng nhau.'],
             ['Bảng đối chiếu công nợ 1 khách hàng (ERP và HRM)', 'Dòng Tổng cộng', 'Bằng nhau. Dòng hợp đồng của bảng đối chiếu có thể khác ở số dư (màn đó không tính 2 cột điều chỉnh vào số dư hợp đồng) - không ghi lỗi.'],
             [M['so_ct'], 'Số dư cuối kỳ của khách', 'Bằng Số dư cuối kỳ dòng Tổng cộng.']],
            widths=[2.4, 1.7, 2.4])
    d.note('Kết quả: ', 'ERP ' + O + '      HRM ' + O)

    d.h2('NT-19. Xuất Excel khớp màn hình')
    d.note('Mục tiêu: ', 'File Excel có đủ dữ liệu theo bộ lọc, số khớp màn hình.')
    d.note('Điều kiện trước: ', 'Lọc kỳ tháng này, không lọc khách hàng (để có nhiều trang).')
    d.table([['Bước', 'Ai / Ở đâu', 'Thao tác'],
             ['1', 'Q - HRM', 'Bấm "Xuất Excel", chọn trường cần xuất (để mặc định đủ cột), bấm xuất.'],
             ['2', 'Q - ERP', 'Bấm Xuất excel, chờ file gửi về email.'],
             ['3', 'Q', 'Mở 2 file, tìm dòng HD-TEST-01 và dòng Tổng cộng.']],
            widths=[0.6, 1.7, 4.2])
    d.bullet('HRM tải file ngay, báo "Xuất Excel thành công"; có đủ mọi trang, không chỉ trang đang xem.')
    d.bullet('Dòng HD-TEST-01 và dòng Tổng cộng trong file HRM bằng màn hình HRM và bằng file ERP.')
    d.bullet('Bỏ trống ô Thời gian rồi bấm Xuất Excel trên HRM: báo "Vui lòng chọn thời gian", không xuất file.')
    d.note('Khác nhau ERP - HRM được chấp nhận: ', 'ERP gửi file qua email, HRM tải ngay và cho chọn cột (chuẩn chung của HRM).')
    d.note('Kết quả: ', 'ERP ' + O + '      HRM ' + O)


# ================================================================================================= phần 5, 6
def chenh_lech(d, man, k):
    d.h1('PHẦN 5: CÁC ĐIỂM KHÁC NHAU ERP - HRM ĐÃ CHỐT')
    d.p('Gặp đúng các hiện tượng dưới đây thì KHÔNG ghi lỗi HRM. Cột "Loại" cho biết vì sao khác: HRM sửa lỗi của ERP, '
        'hoặc HRM theo chuẩn chung của HRM.')
    nhom = 'khách hàng' if k == 'detail' else 'nhân viên'
    rows = [['Điểm', 'ERP', 'HRM', 'Loại'],
            ['Dòng ' + nhom + ' (chữ đậm)', 'Chỉ cộng các hợp đồng trên trang đang xem', 'Cộng đủ mọi hợp đồng theo bộ lọc, mọi trang cùng một tổng', 'Sửa lỗi ERP'],
            ['Số dư đầu kỳ dòng Tổng cộng', ('Tài khoản quyền bộ phận hoặc không quyền thấy số toàn hệ thống' if k == 'detail'
                                             else 'Mọi tài khoản đều thấy số toàn hệ thống'),
             'Chỉ tính trong phạm vi được xem', 'Sửa lỗi bảo mật'],
            ['Ô số tiền bằng 0', 'Hiện "-"' + (', vẫn bấm được' if k == 'detail' else ''), 'Để trống' + (', không bấm được' if k == 'detail' else '') + '; riêng dòng Tổng cộng hiện "0"', 'Chuẩn HRM'],
            ['Xuất Excel', 'Gửi file qua email', 'Tải ngay, cho chọn cột' + ('; "Xuất Excel mẫu in" cũng tải ngay' if k == 'employee' else ''), 'Chuẩn HRM'],
            ['Phân trang', '15 hợp đồng / trang', 'Mặc định 10, chọn được 10 / 20 / 50 / 100', 'Chuẩn HRM'],
            ['Bộ lọc thời gian', 'Hai ô Từ ngày, Đến ngày; bấm Lọc mới tải', 'Một ô Thời gian; chọn xong bảng tự tải', 'Chuẩn HRM'],
            ['Tìm nhanh', 'Không có', 'Có ô tìm theo số hợp đồng, mã hoặc tên khách hàng', 'Chuẩn HRM'],
            ['Chú thích cột', 'Không có', 'Biểu tượng ⓘ ở mỗi đầu cột giải thích cách tính', 'Chuẩn HRM']]
    if k == 'detail':
        rows += [['Hợp đồng lập bên HRM', 'Hiện "-"', 'Hiện mã hợp đồng, bấm mở được', 'Sửa lỗi ERP'],
                 ['Khách hàng không còn trong danh mục', 'Hợp đồng bị dồn nhầm sang khách đứng kế tiếp', 'Có dòng nhóm riêng "Khách hàng #<số>"', 'Sửa lỗi ERP'],
                 ['Tiêu đề cửa sổ chứng từ', 'Luôn "Chi tiết số tiền đã thanh toán"', '"Chi tiết chứng từ" kèm tên cột và hợp đồng / khách hàng', 'Sửa lỗi ERP'],
                 ['Từ ngày lớn hơn Đến ngày', 'Báo lỗi khi bấm Lọc', 'Báo đỏ ngay "Đến ngày phải lớn hơn hoặc bằng Từ ngày.", không tải bảng', 'Chuẩn HRM']]
    else:
        rows += [['Không quyền, sửa đường dẫn để xem nhân viên khác', 'Xem được', 'Không xem được', 'Sửa lỗi bảo mật'],
                 ['Tốc độ khi không lọc gì', 'Có thể 20 giây trở lên', 'Khoảng 5 giây (lọc theo Ngày nghiệm thu vẫn chậm)', 'Cải tiến'],
                 ['Số ngày nợ', 'Tính theo giờ hiện tại', 'Như ERP; xem cách nhau qua mốc ngày có thể lệch 1', 'Giữ như ERP']]
    d.table(rows, widths=[1.6, 1.8, 2.1, 1.0])
    d.h2('Những điểm GIỮ NGUYÊN như ERP (không ghi lỗi ở cả hai hệ thống)')
    d.bullet('Dòng Tổng cộng không áp bộ lọc Số dư cuối kỳ (Dư nợ / Dư có) và không áp ô tìm nhanh.')
    d.bullet('Số dư đầu kỳ của dòng Tổng cộng tính cả phiếu chưa gắn khách hàng / hợp đồng, nên có thể khác tổng các dòng.')
    d.bullet('Phiếu gắn khách hàng nhưng không gắn hợp đồng hiện dòng có dấu "-" ở cột Đơn hàng/hợp đồng.')
    if k == 'detail':
        d.bullet('Phòng ban, Bộ phận, NVKD lấy theo hồ sơ HIỆN TẠI của người lập hợp đồng (nhân viên đã chuyển phòng thì hiện phòng mới).')
    else:
        d.bullet('Hợp đồng có phiếu của nhiều khách hàng thì cột Khách hàng chỉ hiện một khách.')
        d.bullet('Quyền phòng ban / bộ phận tính thêm phòng / bộ phận người xem đang ngồi.')


def bien_ban(d, man, k):
    d.h1('PHẦN 6: BIÊN BẢN TỔNG HỢP KẾT QUẢ NGHIỆM THU')
    d.p('Màn: ' + man['ten'] + '. Ngày nghiệm thu: ……/……/………  Môi trường: ERP test + HRM test (dùng chung dữ liệu).')
    ten = [('NT-01', 'Ghi số nền, so khớp ban đầu'), ('NT-02', 'Xuất bán hàng'), ('NT-03', 'Phiếu chưa hoàn tất'),
           ('NT-04', 'Phiếu thu'), ('NT-05', 'Phiếu báo có'), ('NT-06', 'Điều chỉnh công nợ tăng'),
           ('NT-07', 'Điều chỉnh công nợ giảm'), ('NT-08', 'Khách trả lại hàng'), ('NT-09', 'Phiếu chi trả tiền thừa'),
           ('NT-10', 'Ủy nhiệm chi trả tiền thừa'), ('NT-11', 'Kiểm tổng cả chuỗi'), ('NT-12', 'Thu vượt, lọc Dư nợ / Dư có'),
           ('NT-13', 'Ngày hạch toán, hủy phiếu')]
    ten += ([('NT-14', 'Dòng khách hàng cộng đủ'), ('NT-15', 'Cửa sổ chứng từ'), ('NT-16', 'Hợp đồng HRM, khách ngoài danh mục')]
            if k == 'detail' else
            [('NT-14', 'Gom theo người lập, dòng nhân viên'), ('NT-15', 'Ngày nghiệm thu, Số ngày nợ'), ('NT-16', 'Xuất Excel mẫu in')])
    ten += [('NT-17', 'Phạm vi theo quyền'), ('NT-18', 'Đối chiếu chéo'), ('NT-19', 'Xuất Excel')]
    d.table([['Mã', 'Kịch bản', 'ERP', 'HRM', 'Ghi chú']] + [[a, b, '', '', ''] for a, b in ten],
            widths=[0.7, 2.5, 0.8, 0.8, 1.7])
    d.p('Kết luận: ☐ Đạt, đưa vào sử dụng     ☐ Đạt có điều kiện (ghi rõ)     ☐ Không đạt')
    d.table([['Người test', 'Đại diện nghiệp vụ (kế toán)', 'Đại diện phát triển'],
             ['\n\n\n(Ký, ghi rõ họ tên)', '\n\n\n(Ký, ghi rõ họ tên)', '\n\n\n(Ký, ghi rõ họ tên)']],
            widths=[2.15, 2.2, 2.15])


def build(k):
    man = MAN[k]
    d = HdsdVanXuoi(man['ten'])
    tong_quan(d, man, k)
    chuan_bi(d, man, k)
    luong_chinh(d, man, k)
    (rieng_chi_tiet if k == 'detail' else rieng_theo_nv)(d)
    phan_quyen(d, man, k)
    chenh_lech(d, man, k)
    bien_ban(d, man, k)
    out = os.path.join(HERE, man['file'])
    d.save(out)
    print('OK', out, 'trang:', cap_nhat_truong(out))


if __name__ == '__main__':
    build('detail')
    build('employee')
