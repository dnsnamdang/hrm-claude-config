# -*- coding: utf-8 -*-
"""HDSD man ERP: Bao cao chi phi van chuyen theo nhan vien kinh doanh — ban GON
(skill hdsd-documenter, khuon HDSD_MAU_GON.docx, QgWriter).

Chay:  python ve_so_do.py && python gen_hdsd.py
Anh o hdsd_shots/ (chup ERP local 08/10/2026, tai khoan quyen tong cong ty, ky 06/2026),
icon o hdsd_shots/icons/. Thu muc anh khong commit.
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
OUT = os.path.join(HERE, 'HDSD_Bao cao chi phi van chuyen theo NVKD.docx')
TEN_MAN = 'Báo cáo chi phí vận chuyển theo nhân viên kinh doanh'


def ic(name):
    for d in (ICONS, SHARED_ICONS):
        p = os.path.join(d, name + '.png')
        if os.path.exists(p):
            return ('img', p)
    raise AssertionError('Thiếu icon ' + name)


w = QgWriter(TPL, ROLES, body_from=19,
             cover_replace={'Màn hình: Danh mục khu vực': 'Màn hình: ' + TEN_MAN,
                            'Danh mục khu vực': TEN_MAN})
step = w.step


def sub(segs):
    w.raw('sub', segs)


def img(name, cap):
    w.image(os.path.join(SHOTS, name + '.png'), caption=cap)
    anh_lien_chu_thich(w)


n = [0]


def phan(title):
    n[0] += 1
    h1_trang_moi(w, 'PHẦN %d: %s' % (n[0], title))


# ------------------------------------------------------------------ TỔNG QUAN
h1_trang_moi(w, 'TỔNG QUAN')
w.h2('1. Thuật ngữ sử dụng trong tài liệu')
w.table([['Thuật ngữ', 'Giải thích'],
         ['Cước vận chuyển', 'Tiền vận chuyển kế toán hạch toán cho một chuyến xe và ghi cho một nhân viên kinh doanh chịu.'],
         ['Phiếu hạch toán chuyến xe', 'Phiếu kế toán lập cho chuyến xe chở hàng (giao hàng theo phiếu xuất kho). Mã phiếu hiện ở cột Số chuyến xe.'],
         ['Phiếu hạch toán chuyến xe khác', 'Phiếu kế toán lập cho chuyến xe không chở hàng theo phiếu xuất kho.'],
         ['Ngày hạch toán', 'Ngày ghi trên phiếu hạch toán; báo cáo lọc theo ngày này.'],
         ['Mã công việc', 'Loại chi phí của từng dòng hạch toán. Báo cáo KHÔNG tính các mã: Công lái xe, Xăng xe, Chi phí khác, Vé cầu đường, Công tác phí; cũng không tính dòng không chọn mã công việc.'],
         ['Đối tượng chịu phí', 'Ai chịu phí của dòng hàng trên chuyến: Nhân viên chịu hoặc Công ty chịu.'],
         ['Cấp Phòng ban', 'Dòng chữ đậm (STT 1, 2…): tổng cước của các nhân viên trong phòng.'],
         ['Cấp Nhân viên', 'Dòng chữ xanh (STT 1.1, 1.2…): mã nhân viên, họ tên và tổng cước của nhân viên.'],
         ['Cấp Chuyến', 'Dòng STT 1.1.1…: từng chuyến của nhân viên, chỉ hiện khi tích Show chi tiết.']],
        widths=[2.0, 4.5])
w.h2('2. Cập nhật tài liệu')
w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung'],
         ['1.0', '08/10/2026', 'Đội phát triển phần mềm', 'Tạo mới tài liệu hướng dẫn ' + TEN_MAN + '.']],
        widths=[0.9, 1.1, 1.5, 3.0])
w.h2('3. Quyền sử dụng')
w.table([['Quyền', 'Dữ liệu được xem'],
         ['Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh - Theo tổng công ty (hoặc quyền cũ "Xem báo cáo vận chuyển theo công ty theo tổng công ty")',
          'Mọi công ty; có ô lọc Công ty, Phòng ban, Nhân viên.'],
         ['Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh - Theo công ty (hoặc quyền cũ "Xem báo cáo vận chuyển theo công ty")',
          'Công ty của mình; có ô lọc Phòng ban, Nhân viên.'],
         ['Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh - Theo phòng ban',
          'Phòng ban hiện tại của mình; có ô lọc Nhân viên.'],
         ['Không có quyền nào ở trên', 'Chỉ cước ghi cho chính mình; không có ô lọc Công ty, Phòng ban, Nhân viên.']],
        widths=[3.6, 2.9])
w.h2('4. Sơ đồ luồng số liệu')
img('so_do', 'Sơ đồ luồng số liệu của báo cáo')

# ------------------------------------------------------------------ PHẦN 1
phan('TRUY CẬP VÀ LỌC BÁO CÁO')
step(['Bước 1: Tại menu ', ic('menu_kinhdoanh'), ', chọn ', ic('menu_bcbanhang'), ', chọn ', ic('item_bccpvc')])
sub(['Hoặc tại menu ', ic('menu_kho'), ', chọn ', ic('menu_vcbx'), ', chọn ', ic('item_bccpvc_kho')])
step(['Bước 2: Chọn ', ic('o_tungay'), ' và ', ic('o_denngay'), ' (bắt buộc).'])
step(['Bước 3: Bấm ', ic('btn_loc'), ', hệ thống hiển thị báo cáo theo Phòng ban và Nhân viên.'])
img('01_list', 'Màn hình ' + TEN_MAN)
step(['Bước 4: Chọn thêm điều kiện lọc nếu cần, rồi bấm ', ic('btn_loc')])
sub(['Hoặc chọn ', ic('o_congty'), ' để lọc theo công ty,'])
sub(['Hoặc chọn ', ic('o_phongban'), ' để lọc theo phòng ban,'])
sub(['Hoặc chọn ', ic('o_nhanvien'), ' để lọc theo nhân viên kinh doanh,'])
sub(['Hoặc nhập ', ic('o_sochuyen'), ' để lọc theo mã phiếu hạch toán,'])
sub(['Hoặc nhập ', ic('o_hopdong'), ' để lọc theo mã hợp đồng,'])
sub(['Hoặc nhập ', ic('o_ycxh'), ' để lọc theo mã yêu cầu xuất hàng,'])
sub(['Hoặc chọn ', ic('o_doituong'), ' là Nhân viên chịu hoặc Công ty chịu.'])
step(['Bước 5: Bấm ', ic('btn_lammoi'), ' để xóa ngày và các ô Công ty, Phòng ban, Nhân viên đã chọn.'])

# ------------------------------------------------------------------ PHẦN 2
phan('XEM CHI TIẾT TỪNG CHUYẾN')
step('Bước 1: Lọc báo cáo (xem PHẦN 1).')
step(['Bước 2: Tích ', ic('chk_showchitiet'), ', dưới mỗi nhân viên hiện các chuyến xe.'])
img('02_detail', 'Báo cáo khi tích Show chi tiết')
step('Bước 3: Bấm mã ở cột Yêu cầu xuất hàng để mở phiếu yêu cầu xuất hàng ở thẻ mới.')
sub('Hoặc bấm mã ở cột Hợp đồng để mở hợp đồng ở thẻ mới,')
sub('Hoặc bấm mã ở cột Số chuyến xe để mở phiếu hạch toán chuyến xe ở thẻ mới.')
step(['Bước 4: Bỏ tích ', ic('chk_showchitiet'), ' để ẩn các chuyến.'])

# ------------------------------------------------------------------ PHẦN 3
phan('XUẤT EXCEL')
step('Bước 1: Lọc báo cáo theo dữ liệu cần lấy (xem PHẦN 1).')
step(['Bước 2: Bấm ', ic('btn_xuatexcel'), ', hệ thống mở cửa sổ “Xuất Excel”.'])
img('03_export', 'Cửa sổ Xuất Excel')
step(['Bước 3: Tại ', ic('o_mauexcel'), ' chọn Xuất excel đầy đủ (có từng chuyến) hoặc Xuất excel ngắn gọn (chỉ phòng ban, nhân viên).'])
step(['Bước 4: Bấm ', ic('btn_xuat_modal'), ', trình duyệt mở thẻ mới và tải file Excel về.'])
sub('Hoặc khi kết quả có từ 50 phòng ban trở lên, hệ thống thông báo và gửi file Excel qua email,')
sub(['Hoặc bấm ', ic('btn_dong_modal'), ' để đóng cửa sổ, không xuất.'])

# ------------------------------------------------------------------ PHẦN 4
phan('KIỂM TRA SỐ LIỆU THEO LUỒNG PHÁT SINH')
step('Bước 1: Lọc báo cáo theo khoảng ngày cần kiểm, chọn nhân viên kinh doanh cần kiểm, ghi lại cước hiện tại của nhân viên.')
step('Bước 2: Nhân viên kinh doanh lập yêu cầu xuất hàng theo hợp đồng, kho lập phiếu xuất kho.')
step('Bước 3: Điều vận lập chuyến xe chở hàng cho phiếu xuất kho.')
step('Bước 4: Kế toán lập phiếu hạch toán chuyến xe trong khoảng ngày đang lọc, dòng cước ghi cho nhân viên kinh doanh ở Bước 1, chọn mã công việc cước vận chuyển, hạch toán.')
step(['Bước 5: Bấm ', ic('btn_loc'), ', tích ', ic('chk_showchitiet'),
      ', cước của nhân viên tăng đúng số tiền dòng cước vừa hạch toán và có thêm dòng chuyến mới.'])
img('04_dong_chuyen', 'Dòng chuyến của nhân viên sau khi hạch toán')
sub('Hoặc thêm vào phiếu hạch toán một dòng Xăng xe / Vé cầu đường / Công tác phí cho cùng nhân viên: cước của nhân viên không đổi,')
sub('Hoặc đổi Đến ngày về trước ngày hạch toán của phiếu: chuyến mới không còn trong báo cáo.')
step('Bước 6: So cước nhân viên trên báo cáo với tổng các dòng cước của nhân viên trên các phiếu hạch toán trong khoảng ngày.')

w.rebuild_toc(levels=(1, 2))
print('OK', w.save(OUT))
