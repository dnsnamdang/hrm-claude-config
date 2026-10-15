# -*- coding: utf-8 -*-
"""HDSD 2 bao cao cong no theo MAU VAN XUOI (mau HDSD_YeuCauXuatHang.docx, user dua 12/10/2026 vi QA thay ban
gon 'kho hieu, khong biet test nhu nao cho dung').

Sinh: HDSD_Bang doi chieu cong no 1 khach hang.docx, HDSD_BC tong hop cong no KH theo nhan vien.docx
Chay:  python cat_anh.py && python ve_so_do.py && python gen_hdsd_mau.py
So lieu vi du lay tu anh that (ERP local, ky 06/2026). Khung + ham dung: ../_hdsd_van_xuoi/hdsd_van_xuoi.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_hdsd_van_xuoi'))
from hdsd_van_xuoi import HdsdVanXuoi, cap_nhat_truong  # noqa: E402

SHOTS = os.path.join(HERE, 'hdsd_shots')
NGAY = '12/10/2026'

M_YCXH = 'Khởi tạo › Hàng hóa › Nhập - xuất hàng › "Phiếu Yêu cầu xuất hàng"'
M_YCNH = 'Khởi tạo › Hàng hóa › Nhập - xuất hàng › "Phiếu Yêu cầu nhập hàng"'
M_TIEN = 'Kế toán › Quản lý tiền'
M_DCCN = 'Kế toán › Điều chỉnh công nợ › "Yêu cầu điều chỉnh công nợ"'
M_SO_CT = 'Kế toán › Khách hàng › "Sổ chi tiết công nợ phải thu khách hàng"'


def S(name):
    return os.path.join(SHOTS, name + '.png')


# =====================================================================================================
# PHẦN DÙNG CHUNG CHO 2 BÁO CÁO
# =====================================================================================================
THUAT_NGU = [
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả cho công ty, tính riêng cho từng hợp đồng.'],
    ['Hạch toán', 'Bước kế toán ghi nhận phiếu vào sổ sách. Chỉ phiếu ĐÃ HẠCH TOÁN mới lên báo cáo. Phiếu mới lập, đang chờ duyệt, chưa hạch toán thì báo cáo chưa đổi.'],
    ['Ngày hạch toán', 'Ngày ghi nhận của phiếu. Báo cáo lọc theo ngày này, không theo ngày lập phiếu.'],
    ['Kỳ báo cáo', 'Khoảng Từ ngày - Đến ngày người dùng chọn (lấy trọn cả hai ngày).'],
    ['Số dư đầu kỳ', 'Công nợ cộng dồn từ mọi phiếu có ngày hạch toán TRƯỚC Từ ngày.'],
    ['Phát sinh tăng', 'Phần làm khách nợ thêm trong kỳ: tiền hàng hóa/dịch vụ đã xuất bán, và điều chỉnh tăng công nợ.'],
    ['Phát sinh giảm', 'Phần làm khách bớt nợ trong kỳ: hàng khách trả lại, tiền khách đã thanh toán, và điều chỉnh giảm công nợ.'],
    ['Trả lại tiền thừa', 'Tiền công ty chi trả lại cho khách (phiếu chi, phiếu ủy nhiệm chi). Làm số dư TĂNG lên.'],
    ['Số dư cuối kì', 'Số dư đầu kỳ + Cộng phát sinh tăng - Cộng phát sinh giảm + Trả lại tiền thừa.'],
    ['Dư nợ / Dư có', 'Số dư dương: khách còn nợ công ty (Dư nợ). Số dư âm: khách đã trả thừa (Dư có).'],
    ['YCXH / PXH', 'Phiếu yêu cầu xuất hàng / Phiếu xuất hàng (chứng từ cuối của luồng xuất, nơi ghi nhận công nợ).'],
    ['YCNH / PNH', 'Phiếu yêu cầu nhập hàng / Phiếu nhập hàng (dùng khi khách trả lại hàng).'],
    ['PKT', 'Phiếu kế toán, sinh ra khi kế toán hạch toán điều chỉnh công nợ.'],
    ['ĐCCN', 'Điều chỉnh công nợ.'],
]

# Bảng "phiếu nào làm đổi cột nào" — trái tim của cả 2 báo cáo
NGUON_SO = [
    ['Cột trên báo cáo', 'Thay đổi khi kế toán hạch toán phiếu', 'Hướng'],
    ['Hàng hóa/Dịch vụ (Phát sinh tăng)', 'Phiếu xuất hàng bán theo hợp đồng, phiếu xuất bán hàng mượn, phiếu hạch toán dịch vụ, phiếu hạch toán dịch vụ bảo hành - sửa chữa, biên bản thanh lý, khai báo công nợ đầu kỳ (phần ghi nợ).', 'Tăng nợ'],
    ['Điều chỉnh công nợ (Phát sinh tăng)', 'Yêu cầu điều chỉnh công nợ loại TĂNG, sau khi duyệt và kế toán hạch toán (sinh phiếu kế toán).', 'Tăng nợ'],
    ['Nhập trả lại (Phát sinh giảm)', 'Phiếu nhập hàng khách trả lại theo hợp đồng.', 'Giảm nợ'],
    ['Đã thanh toán (Phát sinh giảm)', 'Phiếu thu, phiếu báo có (tiền khách chuyển khoản), khai báo công nợ đầu kỳ (phần đã thu).', 'Giảm nợ'],
    ['Điều chỉnh công nợ (Phát sinh giảm)', 'Yêu cầu điều chỉnh công nợ loại GIẢM, sau khi duyệt và hạch toán.', 'Giảm nợ'],
    ['Trả lại tiền thừa', 'Phiếu chi, phiếu ủy nhiệm chi trả tiền lại cho khách.', 'Tăng số dư'],
]

LUONG_ERP = [
    ['Bước', 'Chứng từ (ai lập)', 'Ảnh hưởng tới báo cáo'],
    ['1', 'Hợp đồng bán hàng (nhân viên kinh doanh lập, ký với khách)', 'Chưa có số. Hợp đồng là "khung" để gom công nợ.'],
    ['2', 'Phiếu yêu cầu xuất hàng → Đề nghị xuất kho → Phiếu xuất kho → Phiếu xuất hàng (kinh doanh lập yêu cầu, kế toán kho và kho xử lý các bước sau)', 'Khi Phiếu xuất hàng được hạch toán: cột Hàng hóa/Dịch vụ TĂNG.'],
    ['3', 'Phiếu thu / Phiếu báo có (kế toán lập khi khách trả tiền)', 'Khi hạch toán: cột Đã thanh toán TĂNG, số dư GIẢM.'],
    ['4', 'Phiếu yêu cầu nhập hàng khách trả lại → nhập kho → Phiếu nhập hàng (khi khách trả hàng)', 'Khi hạch toán: cột Nhập trả lại TĂNG, số dư GIẢM.'],
    ['5', 'Yêu cầu điều chỉnh công nợ tăng / giảm → duyệt → kế toán hạch toán (phiếu kế toán)', 'Cột Điều chỉnh công nợ ở nhóm tăng hoặc giảm thay đổi.'],
    ['6', 'Phiếu chi / Phiếu ủy nhiệm chi trả lại tiền cho khách', 'Cột Trả lại tiền thừa TĂNG, số dư TĂNG.'],
]


def chuan_bi_du_lieu(d):
    d.h2('5.1. Chuẩn bị trước khi test')
    d.p('Để biết báo cáo đúng hay sai, người test cần một khách hàng và một hợp đồng "sạch" mà mình tự kiểm soát được '
        'mọi phiếu. Khuyến nghị dùng bộ dữ liệu mẫu dưới đây và dùng xuyên suốt PHẦN 5:')
    d.table([['Dữ liệu', 'Giá trị mẫu', 'Ghi chú'],
             ['Khách hàng', 'KH-TEST', 'Khách hàng tạo riêng cho test.'],
             ['Hợp đồng bán hàng', 'HD-TEST-01', 'Do nhân viên A (phòng P1, bộ phận BP1) lập, đã ký.'],
             ['Kỳ lọc', 'Từ ngày = ngày 1 tháng hiện tại; Đến ngày = hôm nay', 'Mọi phiếu test đều hạch toán trong kỳ này, trừ khi kịch bản nói khác.'],
             ['Người lập phiếu kế toán', 'Kế toán (hoặc tài khoản có quyền lập/hạch toán phiếu)', 'Tester không lập được phiếu nào thì nhờ kế toán lập giúp; chỉ cần đúng khách, hợp đồng, số tiền, ngày hạch toán.']],
            widths=[1.6, 2.4, 2.5])
    d.p('Ba quy tắc phải nhớ khi test:')
    d.bullet('Luôn ghi số nền: ', 'trước mỗi bước, lọc báo cáo và chụp lại số liệu. Kết quả đúng là CHÊNH LỆCH so với số nền, không phải con số tuyệt đối (vì hợp đồng có thể đã có phát sinh từ trước).')
    d.bullet('Phiếu phải hạch toán xong: ', 'lập phiếu xong mà chưa duyệt, chưa hạch toán thì báo cáo không đổi — đó là đúng.')
    d.bullet('Để ý ngày hạch toán: ', 'phiếu hạch toán trước Từ ngày đi vào Số dư đầu kỳ; sau Đến ngày thì không được tính.')


def kich_ban_phieu(d, cho_xem, doi_chieu=False):
    """Bảng kịch bản lập phiếu theo luồng chuẩn ERP. doi_chieu=True: ghi điểm riêng của màn Đối chiếu."""
    d.h2('5.2. Kịch bản kiểm tra theo luồng phát sinh chuẩn ERP')
    d.p('Làm lần lượt từng dòng của bảng. Sau mỗi dòng: quay lại báo cáo, giữ nguyên điều kiện lọc, bấm Lọc và so với số '
        'nền ngay trước đó. Chỗ quan sát: ' + cho_xem + '.')
    dc_tang = ('Cột Điều chỉnh công nợ (nhóm tăng) +2,000,000. Dòng Tổng cộng: Số dư cuối kì +2,000,000. '
               'Riêng dòng hợp đồng: Số dư cuối kì KHÔNG đổi (hiện trạng màn này, xem 3.5).') if doi_chieu else \
        'Cột Điều chỉnh công nợ (nhóm tăng) +2,000,000; Cộng tăng +2,000,000; Số dư cuối kì +2,000,000.'
    dc_giam = ('Cột Điều chỉnh công nợ (nhóm giảm) +500,000. Dòng Tổng cộng: Số dư cuối kì -500,000. '
               'Dòng hợp đồng: Số dư cuối kì KHÔNG đổi (hiện trạng).') if doi_chieu else \
        'Cột Điều chỉnh công nợ (nhóm giảm) +500,000; Cộng giảm +500,000; Số dư cuối kì -500,000.'
    them_dong = ' Có thêm 1 dòng chứng từ dưới hợp đồng: ngày hạch toán, mã phiếu.' if doi_chieu else ''
    rows = [['STT', 'Việc cần làm (đường vào)', 'Số tiền', 'Kết quả đúng trên báo cáo'],
            ['1', 'Nhân viên A lập Phiếu yêu cầu xuất hàng cho HD-TEST-01 (menu ' + M_YCXH + '), gửi duyệt. Kế toán kho lập đề nghị xuất kho, kho xuất kho, kế toán lập Phiếu xuất hàng và hạch toán hôm nay.',
             '10,000,000', 'Cột Hàng hóa/Dịch vụ +10,000,000; Số dư cuối kì +10,000,000.' + them_dong +
             (' Số chứng từ dạng "PXH-… (PYCXH-…)".' if doi_chieu else '')],
            ['2', 'Lập thêm một yêu cầu xuất hàng 5,000,000 nhưng CHƯA xuất kho; lập một phiếu thu 1,000,000 nhưng CHƯA duyệt/hạch toán.',
             '—', 'Không cột nào thay đổi.'],
            ['3', 'Kế toán lập Phiếu thu của KH-TEST, chọn hợp đồng HD-TEST-01 (menu ' + M_TIEN + ' › "Phiếu thu"), duyệt và hạch toán hôm nay.',
             '4,000,000', 'Cột Đã thanh toán +4,000,000; Số dư cuối kì -4,000,000.' + them_dong],
            ['4', 'Kế toán lập Phiếu báo có (tiền khách chuyển khoản) cho HD-TEST-01 (menu ' + M_TIEN + ' › "Phiếu báo có"), hạch toán hôm nay.',
             '1,000,000', 'Cột Đã thanh toán +1,000,000; Số dư cuối kì -1,000,000.'],
            ['5', 'Lập Yêu cầu điều chỉnh công nợ TĂNG cho KH-TEST, HD-TEST-01 (menu ' + M_DCCN + '), duyệt đủ cấp, kế toán hạch toán hôm nay.',
             '2,000,000', dc_tang],
            ['6', 'Lập Yêu cầu điều chỉnh công nợ GIẢM cho HD-TEST-01, duyệt và hạch toán hôm nay.', '500,000', dc_giam],
            ['7', 'Khách trả lại hàng: lập Phiếu yêu cầu nhập hàng khách trả lại theo HD-TEST-01 (menu ' + M_YCNH + '), duyệt, kho nhập kho, kế toán lập Phiếu nhập hàng và hạch toán hôm nay.',
             '3,000,000', 'Cột Nhập trả lại +3,000,000; Số dư cuối kì -3,000,000.' + them_dong +
             (' Số chứng từ dạng "PNH-… (PYCNH-…)".' if doi_chieu else '')],
            ['8', 'Kế toán lập Phiếu chi trả lại tiền cho KH-TEST, HD-TEST-01 (menu ' + M_TIEN + ' › "Phiếu chi"), hạch toán hôm nay.',
             '200,000', 'Cột Trả lại tiền thừa +200,000; Số dư cuối kì TĂNG 200,000.'],
            ['9', 'Kế toán lập Phiếu ủy nhiệm chi trả lại tiền cho KH-TEST, HD-TEST-01 (menu ' + M_TIEN + ' › "Phiếu ủy nhiệm chi"), hạch toán hôm nay.',
             '300,000', 'Cột Trả lại tiền thừa +300,000; Số dư cuối kì TĂNG 300,000.']]
    d.table(rows, widths=[0.55, 2.5, 1.1, 2.35])

    d.h2('5.3. Kiểm tổng sau chuỗi phiếu')
    d.p('Sau khi làm xong 9 dòng trên, so Số dư cuối kì của HD-TEST-01 với số nền ban đầu (trước dòng 1). Chênh lệch đúng là:')
    d.p([('+10,000,000 - 4,000,000 - 1,000,000 + 2,000,000 - 500,000 - 3,000,000 + 200,000 + 300,000 = +4,000,000', 'b')])
    if doi_chieu:
        d.p('Riêng màn Đối chiếu: dòng hợp đồng chỉ chênh +2,500,000 vì số dư của dòng hợp đồng không tính 2 cột Điều chỉnh '
            'công nợ (+2,000,000 - 500,000 = +1,500,000 bị bỏ qua). Dòng Tổng cộng vẫn phải chênh đủ +4,000,000.')
    else:
        d.p('Dòng hợp đồng HD-TEST-01, dòng nhân viên A và dòng Tổng cộng đều phải chênh đúng +4,000,000.')

    d.h2('5.4. Các trường hợp KHÔNG được tính')
    d.table([['Tình huống', 'Cách làm', 'Kết quả đúng'],
             ['Phiếu chưa hạch toán', 'Lập phiếu thu nhưng để ở trạng thái chưa duyệt.', 'Báo cáo không đổi. Duyệt và hạch toán xong mới tăng.'],
             ['Phiếu hạch toán trước Từ ngày', 'Phiếu thu 700,000 hạch toán ngày cuối tháng trước. Lọc kỳ tháng này, rồi đổi Từ ngày về ngày 1 tháng trước.',
              ('Lần 1: không nằm ở Đã thanh toán, mà nằm trong Số dư đầu kỳ của dòng Tổng cộng (dòng hợp đồng màn này luôn trống đầu kỳ). Lần 2: chuyển sang cột Đã thanh toán và có dòng chứng từ riêng.'
               if doi_chieu else
               'Lần 1: không nằm ở Đã thanh toán, mà làm Số dư đầu kỳ giảm 700,000. Lần 2: chuyển sang cột Đã thanh toán; Số dư cuối kì không đổi giữa 2 lần.')],
             ['Phiếu hạch toán sau Đến ngày', 'Phiếu thu hạch toán hôm nay; lọc Đến ngày = hôm qua, rồi Đến ngày = hôm nay.', 'Lần 1 không tính; lần 2 có trong Đã thanh toán.'],
             ['Hủy hạch toán / xóa phiếu', 'Kế toán hủy hạch toán (hoặc xóa) phiếu thu 4,000,000 ở dòng 3.', 'Đã thanh toán giảm lại 4,000,000; Số dư cuối kì tăng lại 4,000,000.']],
            widths=[1.5, 2.5, 2.5])


# =====================================================================================================
# BÁO CÁO 1: BẢNG ĐỐI CHIẾU CÔNG NỢ 1 KHÁCH HÀNG
# =====================================================================================================
def bao_cao_doi_chieu():
    TEN = 'Bảng đối chiếu công nợ 1 khách hàng'
    d = HdsdVanXuoi(TEN)
    Q = 'Xem báo cáo đối soát công nợ khách hàng theo '

    d.h1('TỔNG QUAN PHẦN MỀM')
    d.h2('1. Thuật ngữ & viết tắt')
    d.p('Bảng thuật ngữ giúp người dùng hiểu đúng các con số và các bước hướng dẫn.')
    d.table(THUAT_NGU + [
        ['Dòng hợp đồng', 'Dòng chữ đậm (STT 1, 2…): một hợp đồng của khách, cộng các chứng từ bên dưới.'],
        ['Dòng chứng từ', 'Dòng STT 1.1, 1.2…: một phiếu đã hạch toán của hợp đồng trong kỳ, xếp theo ngày.'],
        ['Số dư chạy', 'Số ở cột Số dư cuối kì của dòng chứng từ: số dư của hợp đồng NGAY SAU chứng từ đó.'],
    ], widths=[2.0, 4.5])

    d.h2('2. Lịch sử cập nhật tài liệu')
    d.table([['Phiên bản', 'Ngày', 'Nội dung', 'Người thực hiện'],
             ['1.0', NGAY, 'Khởi tạo HDSD màn ' + TEN + ' (ERP)', 'Phòng Phát triển']], widths=[0.9, 1.1, 3.0, 1.5])

    d.h2('3. Giới thiệu chung & đường dẫn truy cập')
    d.p('Bảng đối chiếu công nợ 1 khách hàng liệt kê TỪNG CHỨNG TỪ làm thay đổi công nợ của một khách hàng trong một kỳ, '
        'gom theo từng hợp đồng: phiếu xuất hàng, phiếu thu, phiếu báo có, phiếu nhập hàng trả lại, phiếu điều chỉnh công nợ, '
        'phiếu chi… Mục đích chính là in hoặc xuất Excel gửi khách hàng ký xác nhận công nợ. Màn chỉ để xem, không sửa dữ liệu.')
    d.bullet('Đường dẫn: ', 'menu Kinh doanh › Báo cáo công nợ › "Bảng đối chiếu công nợ 1 khách hàng".')
    d.bullet('Màn liên quan: ', 'Báo cáo chi tiết công nợ KH, Báo cáo tổng hợp công nợ khách hàng theo nhân viên (cùng menu), '
             'Sổ chi tiết công nợ phải thu khách hàng (menu ' + M_SO_CT + '). Cả 4 màn đọc chung một nguồn số.')
    d.p('Báo cáo không tự tính ra số. Mọi con số đến từ các phiếu đã hạch toán trong luồng bán hàng chuẩn của ERP:')
    d.table(LUONG_ERP, widths=[0.65, 3.2, 2.65])
    d.image(S('so_do_doi_chieu'), 'Sơ đồ luồng số liệu của Bảng đối chiếu công nợ 1 khách hàng')

    d.h2('4. Quyền & phạm vi (tổng quan)')
    d.p('Có 4 quyền xem theo cấp. Ở màn này các quyền chỉ quyết định bộ lọc có thêm những ô nào; màn KHÔNG giới hạn dữ liệu '
        'theo quyền — ai mở được màn cũng tra được công nợ của mọi khách hàng (xem PHẦN 6).')
    d.table([['Tên quyền', 'Ô lọc có thêm'],
             [Q + 'tổng công ty', 'Công ty, Phòng ban, Bộ phận, Nhân viên.'],
             [Q + 'công ty', 'Phòng ban, Bộ phận, Nhân viên.'],
             [Q + 'phòng ban', 'Bộ phận, Nhân viên.'],
             [Q + 'bộ phận', 'Phòng ban, Bộ phận, Nhân viên.'],
             ['Không có quyền nào ở trên', 'Không có ô nào thêm; chỉ có Từ ngày, Đến ngày, Khách hàng, Số hợp đồng.']],
            widths=[3.4, 3.1])

    # ------------------------------------------------------------------------------------------ PHẦN 1
    d.h1('PHẦN 1: TRUY CẬP & BỐ CỤC MÀN HÌNH')
    d.h2('1.1. Cách truy cập')
    d.p('Di chuột vào menu Kinh doanh › Báo cáo công nợ, bấm "Bảng đối chiếu công nợ 1 khách hàng". Màn mở ra với bảng trống '
        '"Chưa có dữ liệu" — báo cáo không tự tải, phải chọn điều kiện rồi bấm Lọc.')
    d.image(S('menu_cong_no'), 'Menu Kinh doanh › Báo cáo công nợ', width=4.2)
    d.h2('1.2. Bố cục màn hình')
    d.bullet('Thanh tiêu đề: ', '"Bảng đối chiếu công nợ 1 khách hàng".')
    d.bullet('Khu vực lọc: ', 'Từ ngày, Đến ngày, Khách hàng (3 ô bắt buộc, có dấu (*)), Số hợp đồng, và các ô Công ty / Phòng ban / Bộ phận / Nhân viên tùy quyền.')
    d.bullet('Hàng nút: ', 'Lọc, Làm mới (nút xanh lá có biểu tượng mũi tên tròn), Xuất Excel, In.')
    d.bullet('Bảng đối chiếu: ', 'dòng Tổng cộng ngay dưới tiêu đề, rồi đến từng hợp đồng và các chứng từ của hợp đồng.')
    d.bullet('Phân trang: ', 'dưới bảng, mỗi trang 15 hợp đồng.')
    d.image(S('dc_01_list'), 'Màn Bảng đối chiếu công nợ 1 khách hàng sau khi lọc (khách 35TNIBDA-5, kỳ 06/2026)')

    # ------------------------------------------------------------------------------------------ PHẦN 2
    d.h1('PHẦN 2: BỘ LỌC & CÁC NÚT')
    d.h2('2.1. Các ô lọc')
    d.table([['Ô lọc', 'Bắt buộc', 'Cách dùng'],
             ['Từ ngày', 'Có', 'Ngày đầu kỳ. Phiếu hạch toán trước ngày này đi vào Số dư đầu kỳ.'],
             ['Đến ngày', 'Có', 'Ngày cuối kỳ (tính trọn ngày). Phiếu hạch toán sau ngày này không được tính.'],
             ['Khách hàng', 'Có', 'Gõ tên, số điện thoại hoặc mã khách để tìm, rồi chọn. Ô cho chọn nhiều khách, nhưng đúng mục đích màn là chọn MỘT khách.'],
             ['Số hợp đồng', 'Không', 'Nhập mã hợp đồng để chỉ xem một hợp đồng của khách.'],
             ['Công ty / Phòng ban / Bộ phận', 'Không', 'Chỉ hiện khi có quyền (mục 4). Lọc hợp đồng theo đơn vị của người lập hợp đồng; ô dưới thu hẹp theo ô trên.'],
             ['Nhân viên', 'Không', 'Chỉ xem hợp đồng do nhân viên đó lập.']],
            widths=[1.7, 0.8, 4.0])
    d.h2('2.2. Khi chưa chọn đủ điều kiện')
    d.p('Bấm Lọc, In hoặc Xuất Excel khi còn trống Từ ngày, Đến ngày hoặc Khách hàng: góc trên bên phải hiện thông báo '
        '"Chưa chọn đủ điều kiện bắt buộc", dưới mỗi ô còn trống hiện chữ đỏ "Bắt buộc chọn". Bảng không tải, không in, không tải file.')
    d.image(S('dc_03_err'), 'Thông báo khi chưa chọn đủ điều kiện bắt buộc')
    d.h2('2.3. Các nút')
    d.table([['Nút', 'Kết quả'],
             ['Lọc', 'Tải bảng đối chiếu theo điều kiện đã chọn.'],
             ['Làm mới (biểu tượng mũi tên tròn)', 'Xóa các ô lọc về trống và xóa các dòng trong bảng.'],
             ['Xuất Excel', 'Tải ngay file Excel "bang_doi_chieu_cong_no_1_khach_hang.xlsx" (đủ mọi trang, có ảnh đầu trang công ty).'],
             ['In', 'Mở thẻ mới với bản in khổ ngang theo mẫu đối soát công nợ, đủ hợp đồng và chứng từ của mọi trang.']],
            widths=[2.2, 4.3])

    # ------------------------------------------------------------------------------------------ PHẦN 3
    d.h1('PHẦN 3: ĐỌC BẢNG ĐỐI CHIẾU')
    d.h2('3.1. Các loại dòng')
    d.table([['Loại dòng', 'Nhận biết', 'Nội dung'],
             ['Tổng cộng', 'Ngay dưới tiêu đề cột, chữ đậm', 'Tổng của khách hàng trên MỌI trang, có Số dư đầu kỳ, tính cả phát sinh không gắn hợp đồng.'],
             ['Hợp đồng', 'STT 1, 2…; mã hợp đồng chữ đậm màu xanh', 'Cộng các chứng từ của hợp đồng trong kỳ. Bấm mã để mở hợp đồng.'],
             ['Chứng từ', 'STT 1.1, 1.2…; có Ngày chứng từ', 'Một phiếu đã hạch toán. Bấm mã để xem phiếu (PHẦN 4).']],
            widths=[1.2, 2.2, 3.1])
    d.h2('3.2. Các cột và số lấy từ đâu')
    d.table([['Cột', 'Ý nghĩa'],
             ['STT', 'Số thứ tự: 1, 2… cho hợp đồng; 1.1, 1.2… cho chứng từ.'],
             ['Ngày chứng từ', 'Ngày hạch toán của phiếu (dòng hợp đồng để trống).'],
             ['Số chứng từ', 'Dòng hợp đồng: mã hợp đồng. Dòng chứng từ: mã phiếu; riêng phiếu xuất hàng, phiếu xuất bán hàng mượn, phiếu nhập hàng có kèm mã phiếu yêu cầu trong ngoặc, vd "PXH-31457 (PYCXH-32487)".'],
             ['Diễn giải', 'Nội dung diễn giải của phiếu.'],
             ['Số dư đầu kỳ', 'Chỉ có số ở dòng Tổng cộng (xem 3.5).']] +
            [[r[0], r[1]] for r in NGUON_SO[1:]] +
            [['Số dư cuối kì', 'Dòng chứng từ: số dư chạy sau chứng từ đó. Dòng hợp đồng: số dư cuối của hợp đồng. Dòng Tổng cộng: số dư cuối của khách.']],
            widths=[2.0, 4.5])
    d.p('Số hiển thị có dấu phẩy ngăn cách hàng nghìn (vd 98,226,000); ô bằng 0 hiện dấu "-".')
    d.h2('3.3. Công thức')
    d.p([('Số dư cuối kì = Số dư đầu kỳ + Hàng hóa/Dịch vụ + Điều chỉnh tăng - Nhập trả lại - Đã thanh toán - Điều chỉnh giảm + Trả lại tiền thừa', 'b')])
    d.p('Công thức đúng nguyên vẹn cho dòng Tổng cộng. Với dòng hợp đồng và dòng chứng từ, màn này bỏ qua 2 cột Điều chỉnh công nợ (xem 3.5).')
    d.h2('3.4. Ví dụ đọc số trên ảnh thật')
    d.p('Dùng Hình 3 (khách 35TNIBDA-5, kỳ 01/06/2026 - 30/06/2026). Kiểm dòng Tổng cộng bằng công thức ở 3.3:')
    d.table([['Thành phần', 'Số trên báo cáo'],
             ['Số dư đầu kỳ', '-101,385,648'],
             ['+ Hàng hóa/Dịch vụ', '196,452,000'],
             ['+ Điều chỉnh công nợ (tăng)', '196,452,000'],
             ['- Nhập trả lại', '98,226,000'],
             ['- Đã thanh toán', '0'],
             ['- Điều chỉnh công nợ (giảm)', '196,452,000'],
             ['+ Trả lại tiền thừa', '0'],
             ['= Số dư cuối kì', '-3,159,648 (khớp dòng Tổng cộng)']], widths=[3.0, 3.5])
    d.p('Đọc hợp đồng số 2 (HĐ_TPE_HN_DAU_26_1044_TP-AMINH 23.6) theo từng chứng từ:')
    d.table([['STT', 'Chứng từ', 'Số tiền', 'Số dư chạy hiển thị'],
             ['2.1', 'PXH-31457 (PYCXH-32487) — phiếu xuất hàng ngày 23/06', 'Hàng hóa/Dịch vụ 98,226,000', '98,226,000'],
             ['2.2', 'TPE.PKT0626.00644 — điều chỉnh giảm ngày 24/06', 'Điều chỉnh giảm 98,226,000', '98,226,000 (không đổi: màn bỏ qua cột điều chỉnh)'],
             ['2.3', 'PNH-11311 (PYCNH-11268) — khách trả hàng ngày 25/06', 'Nhập trả lại 98,226,000', '0 (hiện "-")'],
             ['2.4', 'TPE.PKT0626.00696 — điều chỉnh tăng ngày 26/06', 'Điều chỉnh tăng 98,226,000', '0 (không đổi)']],
            widths=[0.5, 2.6, 1.8, 1.6])
    d.h2('3.5. Những điểm riêng của màn này (hiện trạng, không ghi lỗi)')
    d.bullet('Số dư đầu kỳ của dòng hợp đồng luôn trống: ', 'số dư từ trước kỳ chỉ nằm ở dòng Tổng cộng.')
    d.bullet('Số dư của dòng hợp đồng và số dư chạy không tính 2 cột Điều chỉnh công nợ: ', 'vd hợp đồng số 3 ở Hình 3 có xuất 98,226,000 và điều chỉnh giảm 98,226,000, nếu tính đủ thì số dư bằng 0, nhưng màn hiện 98,226,000.')
    d.bullet('Vì vậy dòng Tổng cộng có thể khác tổng các dòng hợp đồng: ', 'dòng Tổng cộng tính đủ mọi cột, cộng Số dư đầu kỳ và cả phát sinh không gắn hợp đồng. Khi đối chiếu với báo cáo khác, luôn so dòng Tổng cộng.')

    # ------------------------------------------------------------------------------------------ PHẦN 4
    d.h1('PHẦN 4: XEM CHỨNG TỪ, IN & XUẤT EXCEL')
    d.h2('4.1. Xem chứng từ')
    d.p('Bấm mã ở cột Số chứng từ:')
    d.bullet('Phiếu xuất hàng / phiếu xuất bán hàng mượn: ', 'mở cửa sổ "Danh sách hàng hóa: Phiếu xuất hàng - <mã>" liệt kê hàng, số lượng đề nghị, số lượng thực xuất, giá, thành tiền. Nút "Chi Tiết" mở phiếu ở thẻ mới, nút "Hủy" đóng cửa sổ.')
    d.bullet('Chứng từ khác (phiếu thu, phiếu nhập, phiếu kế toán…) và mã hợp đồng: ', 'mở phiếu ở thẻ mới.')
    d.image(S('dc_02_popup'), 'Cửa sổ Danh sách hàng hóa của phiếu xuất hàng')
    d.h2('4.2. Phân trang')
    d.p('Mỗi trang 15 hợp đồng. Dòng Tổng cộng là tổng của mọi trang, không đổi khi chuyển trang.')
    d.h2('4.3. In và Xuất Excel')
    d.table([['Chức năng', 'Nội dung'],
             ['In', 'Bản in khổ ngang theo mẫu đối soát công nợ, đủ hợp đồng và chứng từ của mọi trang, dùng gửi khách ký xác nhận.'],
             ['Xuất Excel', 'Tải ngay file "bang_doi_chieu_cong_no_1_khach_hang.xlsx": ảnh đầu trang công ty, khoảng ngày, bảng như màn hình, đủ mọi trang.']],
            widths=[1.5, 5.0])
    d.p('Cả hai đều cần đủ Từ ngày, Đến ngày, Khách hàng; thiếu thì báo "Chưa chọn đủ điều kiện bắt buộc".')

    # ------------------------------------------------------------------------------------------ PHẦN 5
    d.h1('PHẦN 5: HƯỚNG DẪN KIỂM TRA SỐ LIỆU (DÀNH CHO NGƯỜI TEST)')
    d.p('Phần này hướng dẫn cách chứng minh báo cáo ĐÚNG: tự lập phiếu theo luồng chuẩn của ERP, rồi xem báo cáo thay đổi '
        'có khớp với phiếu vừa lập không. Không cần đọc cơ sở dữ liệu.')
    chuan_bi_du_lieu(d)
    kich_ban_phieu(d, 'dòng hợp đồng HD-TEST-01, dòng chứng từ mới bên dưới và dòng Tổng cộng', doi_chieu=True)
    d.h2('5.5. Đối chiếu chéo với các báo cáo khác')
    d.p('Lọc cùng kỳ, cùng khách KH-TEST ở các màn dưới đây và so số dư cuối kì của khách:')
    d.table([['Màn', 'So cái gì', 'Kết quả đúng'],
             ['Báo cáo chi tiết công nợ KH', 'Dòng Tổng cộng', 'Bằng dòng Tổng cộng của màn này.'],
             ['Báo cáo tổng hợp công nợ khách hàng theo nhân viên (lọc Khách hàng = KH-TEST)', 'Dòng Tổng cộng', 'Bằng dòng Tổng cộng của màn này.'],
             ['Sổ chi tiết công nợ phải thu khách hàng (menu ' + M_SO_CT + ')', 'Số dư cuối kỳ của khách', 'Bằng dòng Tổng cộng của màn này.']],
            widths=[2.6, 1.4, 2.5])
    d.p('Dòng hợp đồng của màn này có thể khác 2 báo cáo kia ở Số dư đầu kỳ và Số dư cuối kì — đúng như 3.5, không ghi lỗi. '
        'Nếu dòng Tổng cộng lệch giữa các màn: ghi số của từng màn vào cột Ghi chú của test case.')
    d.h2('5.6. Kiểm bản in sau khi lập phiếu')
    d.p('Sau chuỗi phiếu ở 5.2, bấm In: bản in có đủ từng phiếu đã lập, đúng ngày hạch toán, đúng số tiền, đúng cột; '
        'dòng Tổng cộng từng cột khớp màn hình.')

    # ------------------------------------------------------------------------------------------ PHẦN 6
    d.h1('PHẦN 6: CÂU HỎI THƯỜNG GẶP & LƯU Ý')
    d.h2('6.1. Câu hỏi thường gặp')
    d.table([['Tình huống', 'Giải thích / cách xử lý'],
             ['Vừa lập phiếu mà báo cáo không đổi', 'Phiếu chưa hạch toán, hoặc ngày hạch toán nằm ngoài kỳ đang lọc. Kiểm trạng thái và ngày hạch toán của phiếu.'],
             ['Dòng hợp đồng không có Số dư đầu kỳ', 'Hiện trạng màn này: số dư từ trước kỳ chỉ nằm ở dòng Tổng cộng.'],
             ['Có điều chỉnh công nợ mà số dư hợp đồng không đổi', 'Hiện trạng: số dư dòng hợp đồng không tính 2 cột Điều chỉnh công nợ; dòng Tổng cộng vẫn tính đủ.'],
             ['Tổng cộng khác tổng các dòng hợp đồng', 'Tổng cộng có thêm Số dư đầu kỳ, 2 cột điều chỉnh, và phát sinh không gắn hợp đồng.'],
             ['Bảng có ít dòng hơn mong đợi', 'Kiểm ô Số hợp đồng / Nhân viên còn giá trị cũ không; bấm Làm mới rồi lọc lại.'],
             ['Cửa sổ Danh sách hàng hóa trống tên hàng', 'Dữ liệu hàng của phiếu không đầy đủ (hay gặp ở dữ liệu thử). Bấm "Chi Tiết" để xem phiếu gốc.']],
            widths=[2.4, 4.1])
    d.h2('6.2. Lỗi đã biết của ERP (gặp đúng hiện tượng thì ghi Failed)')
    d.table([['Hiện tượng', 'Ghi chú'],
             ['Nhân viên không có quyền nào vẫn tra được công nợ của mọi khách hàng.', 'Màn không giới hạn dữ liệu theo quyền.'],
             ['Nhiều trang đầu trống, STT nhảy cóc.', 'Hệ thống chia trang trước rồi mới bỏ các hợp đồng toàn số 0.'],
             ['Cột Diễn giải của phiếu thu / phiếu chi / ủy nhiệm chi luôn trống.', ''],
             ['Bản in: dòng Từ ngày / Đến ngày / Số hợp đồng trống; dòng Tổng cộng đảo chỗ 2 cột Điều chỉnh công nợ.', ''],
             ['Khách có hợp đồng lập bên hệ thống HRM: bấm Lọc báo lỗi, không hiện bảng.', ''],
             ['Bấm Làm mới: các ô lọc trống nhưng dòng Tổng cộng vẫn giữ số của lần lọc trước.', 'Thấy ở Hình 4.']],
            widths=[4.2, 2.3])

    out = os.path.join(HERE, 'HDSD_Bang doi chieu cong no 1 khach hang.docx')
    d.save(out)
    print('OK', out, 'trang:', cap_nhat_truong(out))


# =====================================================================================================
# BÁO CÁO 2: BÁO CÁO TỔNG HỢP CÔNG NỢ KHÁCH HÀNG THEO NHÂN VIÊN
# =====================================================================================================
def bao_cao_theo_nv():
    TEN = 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên'
    d = HdsdVanXuoi(TEN)
    Q = 'Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên - '

    d.h1('TỔNG QUAN PHẦN MỀM')
    d.h2('1. Thuật ngữ & viết tắt')
    d.p('Bảng thuật ngữ giúp người dùng hiểu đúng các con số và các bước hướng dẫn.')
    d.table(THUAT_NGU + [
        ['Nhân viên lập hợp đồng', 'Người tạo hợp đồng bán hàng. Báo cáo gom công nợ theo người này (không theo người phụ trách khách hàng).'],
        ['Ngày nghiệm thu', 'Mốc bắt đầu tính tuổi nợ của hợp đồng (cách xác định ở 3.4).'],
        ['Số ngày nợ', 'Số ngày khách đã nợ kể từ Ngày nghiệm thu + 6 ngày (3.4).'],
    ], widths=[2.0, 4.5])

    d.h2('2. Lịch sử cập nhật tài liệu')
    d.table([['Phiên bản', 'Ngày', 'Nội dung', 'Người thực hiện'],
             ['1.0', NGAY, 'Khởi tạo HDSD màn ' + TEN + ' (ERP)', 'Phòng Phát triển']], widths=[0.9, 1.1, 3.0, 1.5])

    d.h2('3. Giới thiệu chung & đường dẫn truy cập')
    d.p('Báo cáo cho biết mỗi nhân viên kinh doanh đang có những hợp đồng nào còn công nợ, nợ bao nhiêu, nghiệm thu ngày nào '
        'và khách đã nợ bao nhiêu ngày. Dùng để giao nhân viên đi thu nợ. Màn chỉ để xem, không sửa dữ liệu.')
    d.bullet('Đường dẫn: ', 'menu Kinh doanh › Báo cáo công nợ › "Báo cáo tổng hợp công nợ khách hàng theo nhân viên".')
    d.bullet('Màn liên quan: ', 'Báo cáo chi tiết công nợ KH (số của một hợp đồng phải BẰNG NHAU ở 2 màn), Bảng đối chiếu công nợ 1 khách hàng, Sổ chi tiết công nợ phải thu khách hàng.')
    d.p('Mọi con số đến từ các phiếu đã hạch toán trong luồng bán hàng chuẩn của ERP:')
    d.table(LUONG_ERP, widths=[0.65, 3.2, 2.65])
    d.image(S('so_do_theo_nv'), 'Sơ đồ luồng số liệu của Báo cáo tổng hợp công nợ khách hàng theo nhân viên')

    d.h2('4. Quyền & phạm vi (tổng quan)')
    d.p('Mọi tài khoản đều mở được màn. Phạm vi dữ liệu nhìn thấy phụ thuộc quyền; quyền nào cũng thấy thêm hợp đồng do chính mình lập.')
    d.table([['Tên quyền', 'Thấy công nợ của', 'Ô lọc có thêm'],
             [Q + 'tổng công ty', 'Mọi công ty.', 'Công ty, Phòng ban, Bộ phận, Nhân viên'],
             [Q + 'công ty', 'Công ty của mình.', 'Phòng ban, Bộ phận, Nhân viên'],
             [Q + 'phòng ban', 'Phòng đang ngồi + phòng được phân quản lý.', 'Bộ phận, Nhân viên'],
             [Q + 'bộ phận', 'Bộ phận đang ngồi + bộ phận được phân quản lý.', 'Phòng ban, Bộ phận, Nhân viên'],
             ['Không có quyền nào ở trên', 'Chỉ hợp đồng mình lập.', 'Không có']],
            widths=[2.7, 2.1, 1.7])

    # ------------------------------------------------------------------------------------------ PHẦN 1
    d.h1('PHẦN 1: TRUY CẬP & BỐ CỤC MÀN HÌNH')
    d.h2('1.1. Cách truy cập')
    d.p('Di chuột vào menu Kinh doanh › Báo cáo công nợ, bấm "Báo cáo tổng hợp công nợ khách hàng theo nhân viên". Màn mở ra '
        'với bảng trống "Chưa có dữ liệu" — phải chọn Từ ngày, Đến ngày rồi bấm Lọc.')
    d.image(S('menu_cong_no'), 'Menu Kinh doanh › Báo cáo công nợ', width=4.2)
    d.h2('1.2. Bố cục màn hình')
    d.bullet('Khu vực lọc: ', 'Từ ngày, Đến ngày (bắt buộc), Khách hàng, Số hợp đồng, Số dư cuối kỳ, Ngày nghiệm thu, và Công ty / Phòng ban / Bộ phận / Nhân viên tùy quyền.')
    d.bullet('Hàng nút: ', 'Lọc, Làm mới (nút xanh lá biểu tượng mũi tên tròn), Xuất Excel, Xuất Excel Mẫu In.')
    d.bullet('Bảng: ', '16 cột, dòng Tổng cộng ngay dưới tiêu đề; 3 cột đầu (STT, Đơn hàng/hợp đồng, Khách hàng) đứng yên khi kéo ngang.')
    d.bullet('Phân trang: ', 'dưới bảng, mỗi trang 15 dòng hợp đồng.')
    d.image(S('nv_01_list'), 'Màn Báo cáo tổng hợp công nợ khách hàng theo nhân viên (kỳ 06/2026)')

    # ------------------------------------------------------------------------------------------ PHẦN 2
    d.h1('PHẦN 2: BỘ LỌC & CÁC NÚT')
    d.h2('2.1. Các ô lọc')
    d.table([['Ô lọc', 'Bắt buộc', 'Cách dùng'],
             ['Từ ngày', 'Có', 'Ngày đầu kỳ. Phiếu hạch toán trước ngày này đi vào Số dư đầu kỳ.'],
             ['Đến ngày', 'Có', 'Ngày cuối kỳ (tính trọn ngày).'],
             ['Khách hàng', 'Không', 'Gõ tên, số điện thoại hoặc mã khách để chọn; chỉ hiện hợp đồng của khách đó.'],
             ['Số hợp đồng', 'Không', 'Nhập mã hợp đồng.'],
             ['Số dư cuối kỳ', 'Không', 'Dư nợ: chỉ hợp đồng có số dư cuối kì lớn hơn 0. Dư có: chỉ hợp đồng có số dư âm.'],
             ['Ngày nghiệm thu', 'Không', 'Chỉ hợp đồng có Ngày nghiệm thu ĐÚNG BẰNG ngày chọn.'],
             ['Công ty / Phòng ban / Bộ phận', 'Không', 'Chỉ hiện khi có quyền; ô dưới thu hẹp theo ô trên.'],
             ['Nhân viên', 'Không', 'Chỉ nhân viên lập hợp đồng được chọn.']],
            widths=[1.7, 0.8, 4.0])
    d.p('Thiếu Từ ngày hoặc Đến ngày: hệ thống báo "Chưa chọn đủ điều kiện bắt buộc", dưới ô trống hiện "Bắt buộc chọn".')
    d.h2('2.2. Các nút')
    d.table([['Nút', 'Kết quả'],
             ['Lọc', 'Tải báo cáo theo điều kiện đã chọn. Không lọc gì với kỳ dài có thể mất vài chục giây.'],
             ['Làm mới', 'Xóa các ô lọc về trống, xóa các dòng trong bảng.'],
             ['Xuất Excel', 'Thông báo "Báo cáo tổng hợp công nợ khách hàng theo nhân viên sẽ gửi về mail của bạn trong ít phút!" và gửi file qua email (không tải ngay).'],
             ['Xuất Excel Mẫu In', 'Gửi qua email file theo mẫu in: Giá trị hợp đồng thực tế, Giá trị đã thanh toán, Còn nợ cuối kỳ, Ngày nghiệm thu, Số ngày nợ và các cột trống để nhân viên ghi giải trình, kế hoạch thu, xác nhận công nợ.']],
            widths=[1.7, 4.8])

    # ------------------------------------------------------------------------------------------ PHẦN 3
    d.h1('PHẦN 3: ĐỌC BÁO CÁO')
    d.h2('3.1. Các loại dòng')
    d.table([['Loại dòng', 'Nhận biết', 'Nội dung'],
             ['Tổng cộng', 'Ngay dưới tiêu đề cột', 'Tổng của mọi trang, trong phạm vi quyền.'],
             ['Nhân viên', 'STT 1, 2…; chữ đậm "Mã - Họ tên"', 'Người lập hợp đồng; cộng các hợp đồng bên dưới TRÊN TRANG ĐANG XEM.'],
             ['Hợp đồng', 'STT 1.1, 1.2…; mã hợp đồng màu xanh', 'Một hợp đồng còn công nợ, kèm khách hàng "Mã - Tên". Bấm mã để mở hợp đồng.']],
            widths=[1.2, 2.2, 3.1])
    d.h2('3.2. Các cột và số lấy từ đâu')
    d.table([['Cột', 'Ý nghĩa']] +
            [['STT · Đơn hàng/hợp đồng · Khách hàng', 'Định danh dòng. Hợp đồng có phát sinh của nhiều khách thì cột Khách hàng chỉ hiện một khách.'],
             ['Số dư đầu kỳ', 'Công nợ của hợp đồng từ mọi phiếu hạch toán trước Từ ngày.']] +
            [[r[0], r[1]] for r in NGUON_SO[1:3]] +
            [['Cộng (Phát sinh tăng)', 'Hàng hóa/Dịch vụ + Điều chỉnh công nợ (tăng).']] +
            [[r[0], r[1]] for r in NGUON_SO[3:6]] +
            [['Cộng (Phát sinh giảm)', 'Nhập trả lại + Đã thanh toán + Điều chỉnh công nợ (giảm).'],
             [NGUON_SO[6][0], NGUON_SO[6][1]],
             ['Số dư cuối kì', 'Số dư đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa.'],
             ['Ngày nghiệm thu', 'Xem 3.4.'],
             ['Số ngày nợ (Ngày)', 'Xem 3.4.']],
            widths=[2.2, 4.3])
    d.h2('3.3. Ví dụ đọc số trên ảnh thật')
    d.p('Dùng Hình 3 và Hình 4 (kỳ 01/06/2026 - 30/06/2026). Kiểm dòng Tổng cộng:')
    d.table([['Thành phần', 'Số trên báo cáo'],
             ['Số dư đầu kỳ', '298,431,419,064'],
             ['+ Cộng phát sinh tăng (58,216,047,156 + 2,423,770,614)', '60,639,817,770'],
             ['- Cộng phát sinh giảm (2,726,738,570 + 5,517,730,246 + 48,116,777,052)', '56,361,245,868'],
             ['+ Trả lại tiền thừa', '307,836,662'],
             ['= Số dư cuối kì', '303,017,827,628 (khớp dòng Tổng cộng)']], widths=[4.3, 2.2])
    d.p('Kiểm dòng nhân viên: nhân viên 11410102 - Chu Khương Duy có Số dư đầu kỳ -31,702,773 = -9,588,960 (hợp đồng 2.1) '
        '- 20,000,000 (2.2) - 2,113,813 (2.3); các hợp đồng 2.4 trở đi bằng 0. Lưu ý dòng nhân viên chỉ cộng các hợp đồng '
        'đang hiện trên trang.')
    d.image(S('nv_02_right'), 'Kéo ngang để xem Số dư cuối kì, Ngày nghiệm thu, Số ngày nợ')
    d.h2('3.4. Ngày nghiệm thu & Số ngày nợ')
    d.table([['Loại hợp đồng', 'Ngày nghiệm thu lấy từ'],
             ['Hợp đồng hãng cần lắp đặt', 'Ngày của biên bản nghiệm thu bàn giao gần nhất.'],
             ['Hợp đồng hãng không cần lắp đặt', 'Ngày muộn nhất trong: phiếu xuất kho bán theo hợp đồng (ngày duyệt), phiếu xuất bán hàng mượn, phiếu hạch toán dịch vụ.'],
             ['Hợp đồng dịch vụ bảo hành - sửa chữa', 'Ngày muộn nhất trong: hạch toán dịch vụ bảo hành - sửa chữa, phiếu xuất bán hàng mượn, phiếu xuất kho.'],
             ['Không có phiếu nào ở trên', 'Ngày nghiệm thu bàn giao khai trong công nợ đầu kỳ quá hạn; không có thì để trống.']],
            widths=[2.3, 4.2])
    d.p([('Số ngày nợ = Hôm nay - (Ngày nghiệm thu + 6 ngày). ', 'b'),
         'Nhỏ hơn 0 thì hiện 0. Chỉ hiện khi hợp đồng còn dư nợ (Số dư cuối kì lớn hơn 0); hết nợ hoặc không xác định được Ngày nghiệm thu thì để trống. '
         'Ví dụ: nghiệm thu cách hôm nay 30 ngày, còn nợ → Số ngày nợ = 24.'])

    # ------------------------------------------------------------------------------------------ PHẦN 4
    d.h1('PHẦN 4: PHÂN TRANG & XUẤT EXCEL')
    d.h2('4.1. Phân trang')
    d.p('Mỗi trang 15 dòng hợp đồng; nhân viên xếp theo thứ tự tạo tài khoản (không theo bảng chữ cái). Dòng Tổng cộng không đổi '
        'khi chuyển trang; dòng nhân viên chỉ cộng phần hợp đồng của trang đang xem.')
    d.h2('4.2. Xuất Excel')
    d.p('Bấm Xuất Excel hoặc Xuất Excel Mẫu In (xem 2.2). File gửi về email của người đang đăng nhập sau ít phút, có đủ mọi '
        'trang, trong phạm vi quyền của người đó.')

    # ------------------------------------------------------------------------------------------ PHẦN 5
    d.h1('PHẦN 5: HƯỚNG DẪN KIỂM TRA SỐ LIỆU (DÀNH CHO NGƯỜI TEST)')
    d.p('Phần này hướng dẫn cách chứng minh báo cáo ĐÚNG: tự lập phiếu theo luồng chuẩn của ERP, rồi xem báo cáo thay đổi '
        'có khớp với phiếu vừa lập không. Khi test nên lọc Khách hàng = KH-TEST (hoặc Số hợp đồng = HD-TEST-01) để bảng gọn và tải nhanh.')
    chuan_bi_du_lieu(d)
    kich_ban_phieu(d, 'dòng hợp đồng HD-TEST-01, dòng nhân viên A phía trên và dòng Tổng cộng')
    d.h2('5.5. Kiểm Ngày nghiệm thu & Số ngày nợ')
    d.table([['Tình huống', 'Cách làm', 'Kết quả đúng'],
             ['Hợp đồng cần lắp đặt', 'Hợp đồng hãng cần lắp đặt đã xuất hàng; lập biên bản nghiệm thu bàn giao ngày 10/09/2026.', 'Ngày nghiệm thu = 10/09/2026 (theo biên bản, không theo ngày xuất kho).'],
             ['Hợp đồng không cần lắp đặt', 'Có 2 phiếu xuất kho bán theo hợp đồng duyệt ngày 05/09 và 20/09/2026.', 'Ngày nghiệm thu = 20/09/2026.'],
             ['Xuất thêm hàng', 'Xuất kho thêm cho hợp đồng trên, phiếu duyệt hôm nay; lọc lại.', 'Ngày nghiệm thu đổi thành hôm nay; Số ngày nợ = 0.'],
             ['Mới nghiệm thu', 'Ngày nghiệm thu là 3 ngày trước, còn nợ.', 'Số ngày nợ = 0 (không hiện số âm).'],
             ['Thu hết nợ', 'Lập phiếu thu đủ số còn nợ của hợp đồng, hạch toán hôm nay; lọc lại.', 'Số dư cuối kì = 0; Số ngày nợ để trống; Ngày nghiệm thu vẫn hiện.'],
             ['Lọc theo Ngày nghiệm thu', 'Chọn đúng ngày nghiệm thu của hợp đồng, rồi chọn ngày hôm sau.', 'Lần 1 có hợp đồng; lần 2 không có (lọc đúng bằng ngày).']],
            widths=[1.5, 2.6, 2.4])
    d.h2('5.6. Kiểm phạm vi quyền')
    d.table([['Tài khoản', 'Cách làm', 'Kết quả đúng'],
             ['A — không có quyền nào', 'Đăng nhập A, lọc tháng này.', 'Không có ô Công ty, Phòng ban, Bộ phận, Nhân viên; chỉ dòng nhân viên A với hợp đồng của A.'],
             ['B — quyền theo bộ phận, ngồi BP1, quản lý BP2', 'Đăng nhập B, lọc tháng này.', 'Có nhân viên của BP1 và BP2, không có bộ phận khác.'],
             ['C — quyền theo phòng ban, ngồi P1, quản lý P2', 'Đăng nhập C, lọc tháng này.', 'Chỉ có ô Bộ phận, Nhân viên; có nhân viên của P1 và P2.'],
             ['D — quyền theo công ty', 'Đăng nhập D, lọc tháng này.', 'Mọi nhân viên công ty mình, không có công ty khác.'],
             ['E — quyền theo tổng công ty', 'Đăng nhập E, lọc tháng này.', 'Đủ 4 ô lọc tổ chức; nhân viên của mọi công ty.']],
            widths=[1.9, 1.6, 3.0])
    d.h2('5.7. Đối chiếu chéo')
    d.p('Lọc cùng kỳ, cùng hợp đồng HD-TEST-01 ở màn Báo cáo chi tiết công nợ KH: các cột số và Số dư cuối kì của hợp đồng phải '
        'bằng nhau ở 2 màn. Lọc Khách hàng = KH-TEST: dòng Tổng cộng phải bằng dòng Tổng cộng của Bảng đối chiếu công nợ 1 khách hàng '
        'và bằng số dư trên Sổ chi tiết công nợ phải thu khách hàng.')

    # ------------------------------------------------------------------------------------------ PHẦN 6
    d.h1('PHẦN 6: CÂU HỎI THƯỜNG GẶP & LƯU Ý')
    d.h2('6.1. Câu hỏi thường gặp')
    d.table([['Tình huống', 'Giải thích / cách xử lý'],
             ['Vừa lập phiếu mà báo cáo không đổi', 'Phiếu chưa hạch toán, hoặc ngày hạch toán ngoài kỳ đang lọc.'],
             ['Không thấy nhân viên cùng phòng', 'Tài khoản chưa có quyền xem theo phòng ban / bộ phận; không có quyền thì chỉ thấy hợp đồng mình lập.'],
             ['Hợp đồng nằm dưới nhân viên "lạ"', 'Báo cáo gom theo người LẬP hợp đồng, không theo người phụ trách khách hàng hiện tại.'],
             ['Dòng nhân viên không bằng tổng các hợp đồng của họ', 'Dòng nhân viên chỉ cộng các hợp đồng trên trang đang xem; hợp đồng ở trang sau không được cộng vào.'],
             ['Số ngày nợ trống', 'Hợp đồng đã hết nợ, hoặc chưa xác định được Ngày nghiệm thu.'],
             ['Bấm Xuất Excel không thấy tải file', 'Đúng thiết kế: file gửi qua email sau ít phút.'],
             ['Lọc rất lâu', 'Không lọc gì với kỳ dài thì chậm. Thêm điều kiện Khách hàng / Nhân viên / Số hợp đồng.']],
            widths=[2.4, 4.1])
    d.h2('6.2. Lỗi đã biết của ERP (gặp đúng hiện tượng thì ghi Failed)')
    d.table([['Hiện tượng', 'Ghi chú'],
             ['Số dư đầu kỳ của dòng Tổng cộng luôn là số của toàn hệ thống, kể cả với người chỉ có quyền phòng ban hoặc không có quyền.', 'Các cột khác của dòng Tổng cộng vẫn theo phạm vi quyền.'],
             ['Không lọc gì với kỳ dài: tải mất 20 giây trở lên.', ''],
             ['Người không có quyền tự sửa đường dẫn xuất Excel thêm nhân viên khác thì nhận được file có hợp đồng của nhân viên đó.', 'Dành cho tester kỹ thuật.']],
            widths=[4.2, 2.3])

    out = os.path.join(HERE, 'HDSD_BC tong hop cong no KH theo nhan vien.docx')
    d.save(out)
    print('OK', out, 'trang:', cap_nhat_truong(out))


if __name__ == '__main__':
    bao_cao_doi_chieu()
    bao_cao_theo_nv()
