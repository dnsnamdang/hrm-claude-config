# -*- coding: utf-8 -*-
"""HDSD man ERP goc — 2 bao cao cong no khach hang, ban GON (skill hdsd-documenter, khuon HDSD_MAU_GON.docx,
QgWriter; khuon theo erp-bao-cao-chi-phi-van-chuyen-theo-nvkd/gen_hdsd.py).

Sinh: HDSD_Bang doi chieu cong no 1 khach hang.docx, HDSD_BC tong hop cong no KH theo nhan vien.docx
Chay:  python cat_anh.py && python ve_so_do.py && python gen_hdsd.py
Anh o hdsd_shots/ (chup ERP local 12/10/2026, tai khoan quyen tong cong ty, ky 06/2026). Thu muc anh khong commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'hrm', '.plans', 'gop-db', '_catalog_docs_lib'))
sys.path.insert(0, LIB)
from qg_writer import QgWriter  # noqa: E402
from hdsd_gon import h1_trang_moi, anh_lien_chu_thich, TPL, ROLES, SHARED_ICONS  # noqa: E402

SHOTS = os.path.join(HERE, 'hdsd_shots')
ICONS = os.path.join(SHOTS, 'icons')
NGAY = '12/10/2026'

THUAT_NGU_CHUNG = [
    ['Công nợ phải thu', 'Số tiền khách hàng còn phải trả cho công ty, theo từng hợp đồng.'],
    ['Hạch toán', 'Kế toán ghi nhận phiếu vào sổ sách. Chỉ phiếu đã hạch toán mới lên báo cáo; phiếu mới lập, chờ duyệt thì chưa.'],
    ['Ngày hạch toán', 'Ngày ghi nhận của phiếu; báo cáo lọc theo ngày này.'],
    ['Số dư đầu kỳ', 'Công nợ tính từ mọi phiếu có ngày hạch toán trước Từ ngày.'],
    ['Phát sinh tăng', 'Hàng hóa/Dịch vụ: phiếu xuất kho bán hàng, phiếu xuất bán hàng mượn, phiếu hạch toán dịch vụ, biên bản thanh lý. Điều chỉnh công nợ: phiếu điều chỉnh ghi tăng nợ khách.'],
    ['Phát sinh giảm', 'Nhập trả lại: phiếu nhập hàng khách trả lại. Đã thanh toán: phiếu thu, phiếu báo có. Điều chỉnh công nợ: phiếu điều chỉnh ghi giảm nợ khách.'],
    ['Trả lại tiền thừa', 'Phiếu chi, phiếu ủy nhiệm chi trả tiền lại cho khách; làm số dư tăng lên.'],
    ['Số dư cuối kì', 'Đầu kỳ + Cộng tăng - Cộng giảm + Trả lại tiền thừa. Số dương: khách còn nợ (Dư nợ); số âm: khách trả thừa (Dư có).'],
]


def tao_writer(ten_man):
    w = QgWriter(TPL, ROLES, body_from=19,
                 cover_replace={'Màn hình: Danh mục khu vực': 'Màn hình: ' + ten_man,
                                'Danh mục khu vực': ten_man})
    n = [0]

    def ic(name):
        for d in (ICONS, SHARED_ICONS):
            p = os.path.join(d, name + '.png')
            if os.path.exists(p):
                return ('img', p)
        raise AssertionError('Thiếu icon ' + name)

    def sub(segs):
        w.raw('sub', segs)

    def img(name, cap):
        w.image(os.path.join(SHOTS, name + '.png'), caption=cap)
        anh_lien_chu_thich(w)

    def phan(title):
        n[0] += 1
        h1_trang_moi(w, 'PHẦN %d: %s' % (n[0], title))

    return w, ic, sub, img, phan


def tong_quan(w, img, ten_man, thuat_ngu_rieng, quyen, so_do):
    h1_trang_moi(w, 'TỔNG QUAN')
    w.h2('1. Thuật ngữ sử dụng trong tài liệu')
    w.table([['Thuật ngữ', 'Giải thích']] + THUAT_NGU_CHUNG + thuat_ngu_rieng, widths=[2.0, 4.5])
    w.h2('2. Cập nhật tài liệu')
    w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung'],
             ['1.0', NGAY, 'Đội phát triển phần mềm', 'Tạo mới tài liệu hướng dẫn ' + ten_man + '.']],
            widths=[0.9, 1.1, 1.5, 3.0])
    w.h2('3. Quyền sử dụng')
    w.table([['Quyền', 'Dữ liệu được xem']] + quyen, widths=[3.6, 2.9])
    w.h2('4. Sơ đồ luồng số liệu')
    img(so_do, 'Sơ đồ luồng số liệu của báo cáo')


def luong_erp(w, ic, sub, img, step, cho_xem, them_buoc_cuoi):
    """Phan kiem tra so lieu theo luong nghiep vu chuan ERP: lap phieu goc -> hach toan -> loc lai bao cao."""
    step('Bước 1: Lọc báo cáo theo khoảng ngày cần kiểm và khách hàng cần kiểm, ghi lại số liệu hiện tại ở ' + cho_xem + ' (gọi là số nền).')
    step('Bước 2: Lập phiếu làm TĂNG công nợ theo luồng bán hàng:')
    sub('Nhân viên kinh doanh lập phiếu yêu cầu xuất hàng theo hợp đồng của khách (menu Khởi tạo > Hàng hóa > Nhập - xuất hàng > Phiếu Yêu cầu xuất hàng), trình duyệt,')
    sub('Kho lập và duyệt phiếu xuất kho cho yêu cầu đó, ngày hạch toán nằm trong khoảng ngày đang lọc.')
    step(['Bước 3: Bấm ', ic('btn_loc'), ', cột Hàng hóa/Dịch vụ và Số dư cuối kì tăng đúng giá trị phiếu xuất so với số nền.'])
    step('Bước 4: Lập phiếu làm GIẢM công nợ, hạch toán trong khoảng ngày đang lọc, rồi lọc lại:')
    sub('Phiếu thu hoặc phiếu báo có của khách, chọn đúng hợp đồng (menu Kế toán > Quản lý tiền): cột Đã thanh toán tăng, Số dư cuối kì giảm đúng số tiền,')
    sub('Hoặc phiếu yêu cầu nhập hàng khách trả lại theo hợp đồng, kho nhập kho (menu Khởi tạo > Hàng hóa > Nhập - xuất hàng > Phiếu Yêu cầu nhập hàng): cột Nhập trả lại tăng, Số dư cuối kì giảm,')
    sub('Hoặc yêu cầu điều chỉnh công nợ giảm (menu Kế toán > Điều chỉnh công nợ > Yêu cầu điều chỉnh công nợ), duyệt đủ cấp: cột Điều chỉnh công nợ ở nhóm Phát sinh giảm tăng.')
    step('Bước 5: Lập phiếu chi hoặc phiếu ủy nhiệm chi trả lại tiền thừa cho khách, lọc lại: cột Trả lại tiền thừa tăng, Số dư cuối kì TĂNG đúng số tiền.')
    step('Bước 6: Kiểm các trường hợp không được tính:')
    sub('Phiếu mới lập, chưa duyệt, chưa hạch toán: báo cáo không đổi,')
    sub('Phiếu có ngày hạch toán trước Từ ngày: không nằm ở cột phát sinh mà nằm trong Số dư đầu kỳ,')
    sub('Phiếu có ngày hạch toán sau Đến ngày: không được tính,')
    sub('Kế toán hủy hạch toán hoặc xóa phiếu: số liệu trở về như trước khi lập phiếu.')
    for b in them_buoc_cuoi:
        b()


# =============================================================== BÁO CÁO 1: ĐỐI CHIẾU
def bao_cao_doi_chieu():
    TEN = 'Bảng đối chiếu công nợ 1 khách hàng'
    w, ic, sub, img, phan = tao_writer(TEN)
    step = w.step
    tong_quan(w, img, TEN, [
        ['Dòng hợp đồng', 'Dòng chữ đậm (STT 1, 2…): mã hợp đồng của khách và tổng phát sinh của hợp đồng.'],
        ['Dòng chứng từ', 'Dòng STT 1.1, 1.2…: từng phiếu đã hạch toán của hợp đồng trong kỳ, xếp theo ngày. Cột Số dư cuối kì của dòng này là số dư sau chứng từ đó.'],
        ['Dòng Tổng cộng', 'Dòng ngay dưới tiêu đề bảng: tổng của khách hàng, tính cả Số dư đầu kỳ và cả phát sinh không gắn hợp đồng.'],
    ], [
        ['Xem báo cáo đối soát công nợ khách hàng theo tổng công ty', 'Có ô lọc Công ty, Phòng ban, Bộ phận, Nhân viên.'],
        ['Xem báo cáo đối soát công nợ khách hàng theo công ty', 'Có ô lọc Phòng ban, Bộ phận, Nhân viên.'],
        ['Xem báo cáo đối soát công nợ khách hàng theo phòng ban', 'Có ô lọc Bộ phận, Nhân viên.'],
        ['Xem báo cáo đối soát công nợ khách hàng theo bộ phận', 'Có ô lọc Phòng ban, Bộ phận, Nhân viên.'],
        ['Không có quyền nào ở trên', 'Vẫn mở được màn, chỉ có ô Từ ngày, Đến ngày, Khách hàng, Số hợp đồng.'],
    ], 'so_do_doi_chieu')

    phan('TRUY CẬP VÀ LỌC BÁO CÁO')
    step(['Bước 1: Tại menu ', ic('menu_kinhdoanh'), ', chọn ', ic('menu_bccongno'), ', chọn ', ic('item_doichieu')])
    img('menu_cong_no', 'Đường vào nhóm Báo cáo công nợ')
    step(['Bước 2: Chọn ', ic('o_tungay'), ' và ', ic('o_denngay'), ' (bắt buộc).'])
    step(['Bước 3: Tại ', ic('o_khachhang'), ' gõ tên, số điện thoại hoặc mã khách hàng, chọn khách cần đối chiếu (bắt buộc).'])
    step(['Bước 4: Bấm ', ic('btn_loc'), ', hệ thống hiển thị các hợp đồng của khách và từng chứng từ phát sinh trong kỳ.'])
    img('dc_01_list', 'Màn hình ' + TEN)
    sub('Nếu thiếu Từ ngày, Đến ngày hoặc Khách hàng: hệ thống thông báo “Chưa chọn đủ điều kiện bắt buộc” và hiện “Bắt buộc chọn” dưới ô còn trống.')
    img('dc_03_err', 'Thông báo khi chưa chọn đủ điều kiện bắt buộc')
    step(['Bước 5: Chọn thêm điều kiện lọc nếu cần, rồi bấm ', ic('btn_loc')])
    sub(['Hoặc nhập ', ic('o_sohopdong'), ' để chỉ xem một hợp đồng,'])
    sub(['Hoặc chọn ', ic('o_congty'), ', ', ic('o_phongban'), ', ', ic('o_bophan'), ' để lọc theo đơn vị của người lập hợp đồng,'])
    sub(['Hoặc chọn ', ic('o_nhanvien'), ' để chỉ xem hợp đồng do nhân viên đó lập.'])
    step(['Bước 6: Bấm ', ic('btn_lammoi'), ' để xóa các điều kiện đã chọn.'])

    phan('XEM CHỨNG TỪ')
    step('Bước 1: Lọc báo cáo (xem PHẦN 1).')
    step('Bước 2: Đọc từng dòng chứng từ dưới mỗi hợp đồng:')
    sub('Ngày chứng từ là ngày hạch toán của phiếu,')
    sub('Phiếu xuất kho, phiếu xuất bán hàng mượn, phiếu nhập trả lại hiện mã phiếu kèm mã phiếu yêu cầu trong ngoặc,')
    sub('Số tiền nằm ở đúng cột theo loại phiếu (xem bảng Thuật ngữ); cột Số dư cuối kì là số dư sau chứng từ đó.')
    step('Bước 3: Bấm mã của phiếu xuất kho hoặc phiếu xuất bán hàng mượn, hệ thống mở cửa sổ “Danh sách hàng hóa” của phiếu.')
    img('dc_02_popup', 'Cửa sổ Danh sách hàng hóa của phiếu xuất')
    sub(['Bấm ', ic('btn_chitiet'), ' để mở phiếu ở thẻ mới,'])
    sub(['Hoặc bấm ', ic('btn_huy'), ' để đóng cửa sổ.'])
    step('Bước 4: Bấm mã của chứng từ khác (phiếu thu, phiếu nhập, phiếu điều chỉnh…) hoặc mã hợp đồng để mở phiếu ở thẻ mới.')
    step('Bước 5: Khi khách có nhiều hơn 15 hợp đồng, dùng thanh phân trang dưới bảng để xem tiếp.')

    phan('IN VÀ XUẤT EXCEL')
    step('Bước 1: Lọc báo cáo theo khách hàng và kỳ cần gửi đối chiếu (xem PHẦN 1).')
    step(['Bước 2: Bấm ', ic('btn_in'), ', trình duyệt mở thẻ mới với bản in khổ ngang theo mẫu đối soát công nợ, gồm đủ hợp đồng và chứng từ của mọi trang.'])
    step(['Bước 3: Bấm ', ic('btn_xuatexcel'), ', trình duyệt tải ngay file Excel bảng đối chiếu.'])
    sub('Nếu chưa chọn đủ Từ ngày, Đến ngày, Khách hàng: hệ thống thông báo “Chưa chọn đủ điều kiện bắt buộc”, không in, không tải file.')
    step('Bước 4: Gửi bản in hoặc file cho khách xác nhận công nợ.')

    phan('KIỂM TRA SỐ LIỆU THEO LUỒNG PHÁT SINH')

    def doi_chieu_them():
        step('Bước 7: Sau mỗi phiếu đã hạch toán, dưới hợp đồng có thêm một dòng chứng từ: đúng ngày hạch toán, đúng mã phiếu, số tiền ở đúng cột; bấm mã mở đúng phiếu.')
        step('Bước 8: So dòng Tổng cộng với các báo cáo công nợ khác cùng kỳ, cùng khách:')
        sub('Số dư cuối kì của dòng Tổng cộng bằng số trên Báo cáo chi tiết công nợ KH, Báo cáo tổng hợp công nợ khách hàng theo nhân viên và Sổ chi tiết công nợ phải thu khách hàng,')
        sub('Riêng dòng hợp đồng của màn này: Số dư đầu kỳ để trống và số dư không tính 2 cột Điều chỉnh công nợ, nên có thể khác tổng các dòng hợp đồng ở hai báo cáo kia.')
        step(['Bước 9: Bấm ', ic('btn_in'), ', bản in có đủ từng phiếu vừa lập, đúng ngày, đúng số tiền, đúng cột.'])

    luong_erp(w, ic, sub, img, step, 'dòng hợp đồng và dòng Tổng cộng', [doi_chieu_them])

    out = os.path.join(HERE, 'HDSD_Bang doi chieu cong no 1 khach hang.docx')
    w.rebuild_toc(levels=(1, 2))
    print('OK', w.save(out))


# =============================================================== BÁO CÁO 2: THEO NHÂN VIÊN
def bao_cao_theo_nv():
    TEN = 'Báo cáo tổng hợp công nợ khách hàng theo nhân viên'
    w, ic, sub, img, phan = tao_writer(TEN)
    step = w.step
    Q = 'Xem báo cáo tổng hợp công nợ khách hàng theo nhân viên - '
    tong_quan(w, img, TEN, [
        ['Dòng nhân viên', 'Dòng chữ đậm (STT 1, 2…): mã - họ tên nhân viên lập hợp đồng, cộng các hợp đồng bên dưới trên trang đang xem.'],
        ['Dòng hợp đồng', 'Dòng STT 1.1, 1.2…: mã hợp đồng, khách hàng (mã - tên) và công nợ của hợp đồng.'],
        ['Ngày nghiệm thu', 'Hợp đồng cần lắp đặt: ngày biên bản nghiệm thu bàn giao gần nhất. Hợp đồng không cần lắp đặt: ngày xuất hàng / hạch toán dịch vụ muộn nhất.'],
        ['Số ngày nợ', 'Hôm nay - (Ngày nghiệm thu + 6 ngày), nhỏ hơn 0 thì hiện 0; chỉ hiện khi hợp đồng còn dư nợ.'],
    ], [
        [Q + 'tổng công ty', 'Mọi công ty; có ô lọc Công ty, Phòng ban, Bộ phận, Nhân viên.'],
        [Q + 'công ty', 'Công ty của mình và hợp đồng mình lập; có ô lọc Phòng ban, Bộ phận, Nhân viên.'],
        [Q + 'phòng ban', 'Phòng đang ngồi, phòng được phân quản lý và hợp đồng mình lập; có ô lọc Bộ phận, Nhân viên.'],
        [Q + 'bộ phận', 'Bộ phận đang ngồi, bộ phận được phân quản lý và hợp đồng mình lập.'],
        ['Không có quyền nào ở trên', 'Chỉ hợp đồng mình lập; không có ô lọc Công ty, Phòng ban, Bộ phận, Nhân viên.'],
    ], 'so_do_theo_nv')

    phan('TRUY CẬP VÀ LỌC BÁO CÁO')
    step(['Bước 1: Tại menu ', ic('menu_kinhdoanh'), ', chọn ', ic('menu_bccongno'), ', chọn ', ic('item_theonv')])
    img('menu_cong_no', 'Đường vào nhóm Báo cáo công nợ')
    step(['Bước 2: Chọn ', ic('o_tungay'), ' và ', ic('o_denngay'), ' (bắt buộc).'])
    sub('Nếu để trống: hệ thống thông báo “Chưa chọn đủ điều kiện bắt buộc” và hiện “Bắt buộc chọn” dưới ô trống.')
    step(['Bước 3: Bấm ', ic('btn_loc'), ', hệ thống hiển thị công nợ theo nhân viên lập hợp đồng và từng hợp đồng.'])
    img('nv_01_list', 'Màn hình ' + TEN)
    step(['Bước 4: Chọn thêm điều kiện lọc nếu cần, rồi bấm ', ic('btn_loc')])
    sub(['Hoặc chọn ', ic('o_khachhang'), ' để xem công nợ của một khách,'])
    sub(['Hoặc nhập ', ic('o_sohopdong'), ' để xem một hợp đồng,'])
    sub(['Hoặc chọn ', ic('o_soducuoiky'), ' là Dư nợ (khách còn nợ) hoặc Dư có (khách trả thừa),'])
    sub(['Hoặc chọn ', ic('o_ngaynghiemthu'), ' để xem các hợp đồng nghiệm thu đúng ngày đó,'])
    sub(['Hoặc chọn ', ic('o_congty'), ', ', ic('o_phongban'), ', ', ic('o_bophan'), ', ', ic('o_nhanvien'), ' để lọc theo đơn vị, nhân viên.'])
    step(['Bước 5: Bấm ', ic('btn_lammoi'), ' để xóa các điều kiện đã chọn.'])

    phan('XEM CÔNG NỢ VÀ SỐ NGÀY NỢ')
    step('Bước 1: Lọc báo cáo (xem PHẦN 1).')
    step('Bước 2: Đọc dòng Tổng cộng dưới tiêu đề bảng: tổng của mọi trang.')
    step('Bước 3: Đọc dòng nhân viên (chữ đậm) và các hợp đồng của nhân viên bên dưới; bấm mã hợp đồng để mở hợp đồng ở thẻ mới.')
    step('Bước 4: Kéo thanh cuộn ngang của bảng sang phải để xem Số dư cuối kì, Ngày nghiệm thu, Số ngày nợ (3 cột đầu STT, Đơn hàng/hợp đồng, Khách hàng đứng yên).')
    img('nv_02_right', 'Các cột Số dư cuối kì, Ngày nghiệm thu, Số ngày nợ')
    step('Bước 5: Dùng thanh phân trang dưới bảng để xem tiếp (15 hợp đồng mỗi trang).')

    phan('XUẤT EXCEL')
    step('Bước 1: Lọc báo cáo theo dữ liệu cần lấy (xem PHẦN 1).')
    step(['Bước 2: Bấm ', ic('btn_xuatexcel'), ', hệ thống thông báo “Báo cáo tổng hợp công nợ khách hàng theo nhân viên sẽ gửi về mail của bạn trong ít phút!” và gửi file qua email.'])
    sub(['Hoặc bấm ', ic('btn_xuatexcel_mauin'), ' để nhận file theo mẫu in qua email: có Giá trị hợp đồng thực tế, Giá trị đã thanh toán, Còn nợ cuối kỳ, Ngày nghiệm thu, Số ngày nợ và các cột trống để nhân viên ghi giải trình, kế hoạch thu, xác nhận công nợ.'])
    step('Bước 3: Mở email, tải file; số liệu khớp màn hình và đủ mọi trang.')

    phan('KIỂM TRA SỐ LIỆU THEO LUỒNG PHÁT SINH')

    def theo_nv_them():
        step('Bước 7: Kiểm Ngày nghiệm thu và Số ngày nợ:')
        sub('Hợp đồng cần lắp đặt: lập biên bản nghiệm thu bàn giao, lọc lại, Ngày nghiệm thu bằng ngày biên bản,')
        sub('Hợp đồng không cần lắp đặt: xuất kho thêm cho hợp đồng, lọc lại, Ngày nghiệm thu đổi thành ngày duyệt phiếu xuất mới, Số ngày nợ về 0,')
        sub('Lập phiếu thu đủ số còn nợ của hợp đồng, lọc lại: Số dư cuối kì bằng 0, cột Số ngày nợ để trống.')
        step('Bước 8: Nhân viên lập hợp đồng mới cho khách và xuất kho trong kỳ, lọc lại: hợp đồng mới hiện dưới đúng dòng nhân viên đó, dòng nhân viên tăng tương ứng.')
        step('Bước 9: Lọc cùng kỳ, cùng hợp đồng ở Báo cáo chi tiết công nợ KH: số liệu các cột của hợp đồng bằng nhau ở hai báo cáo.')
        step('Bước 10: Đăng nhập tài khoản chỉ có quyền theo phòng ban (hoặc không có quyền), lọc lại: chỉ thấy hợp đồng trong phạm vi quyền (xem TỔNG QUAN mục 3).')

    luong_erp(w, ic, sub, img, step, 'dòng hợp đồng, dòng nhân viên lập hợp đồng và dòng Tổng cộng', [theo_nv_them])

    out = os.path.join(HERE, 'HDSD_BC tong hop cong no KH theo nhan vien.docx')
    w.rebuild_toc(levels=(1, 2))
    print('OK', w.save(out))


if __name__ == '__main__':
    bao_cao_doi_chieu()
    bao_cao_theo_nv()
