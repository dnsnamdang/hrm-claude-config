# -*- coding: utf-8 -*-
"""HDSD Quy trình phê duyệt BOM list — bản GỌN (khuôn HDSD_MAU_GON.docx). Chạy: python3 gen_hdsd.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, '..', '..', '_catalog_docs_lib')
sys.path.insert(0, LIB)
from qg_writer import QgWriter, strip_embedded_fonts  # noqa: E402
from hdsd_gon import TPL, ROLES, h1_trang_moi, anh_lien_chu_thich  # noqa: E402

SHOTS = os.path.join(HERE, 'shots')
ICONS = [os.path.join(HERE, 'icons'), os.path.join(HERE, '..', '..', 'catalog-docs-v2', 'icons')]
OUT = os.path.join(HERE, 'HDSD_QuyTrinh_PheDuyetBomList.docx')


def ic(name):
    for d in ICONS:
        p = os.path.join(d, name + '.png')
        if os.path.exists(p):
            return ('img', p)
    raise AssertionError('Thiếu icon ' + name)


w = QgWriter(TPL, ROLES, body_from=19, cover_replace={'Danh mục khu vực': 'Quy trình phê duyệt BOM list'})
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


MENU = ['Từ phân hệ CÔNG VIỆC ', ic('menu_phanhe'), ', tại menu Làm giải pháp ', ic('menu_lam_giai_phap'), ', chọn ']


def vao_bom(k=1):
    step(['Bước %d: ' % k] + MENU + ['BOM Giải pháp ', ic('item_bom_gp')])


def vao_gp(k=1):
    step(['Bước %d: ' % k] + MENU + ['Quản lý giải pháp ', ic('item_quan_ly_gp')])
    step(['Bước %d: Bấm ' % (k + 1), ic('btn_quan_ly_gp_row'),
          ' (Quản lý giải pháp) ở cột Hành động của giải pháp cần xử lý'])


# ------------------------------------------------------------------ TỔNG QUAN
h1_trang_moi(w, 'TỔNG QUAN')
w.h2('1. Thuật ngữ sử dụng trong tài liệu')
w.table([
    ['Thuật ngữ', 'Giải thích'],
    ['BOM list (BOM)', 'Danh sách hàng hoá, dịch vụ cần dùng cho giải pháp / hạng mục của dự án'],
    ['BOM thành phần', 'BOM lập trực tiếp từ hàng hoá, là phần con để gộp vào BOM tổng hợp'],
    ['BOM tổng hợp cấp hạng mục', 'BOM gộp các BOM thành phần của một hạng mục, được gửi duyệt theo hồ sơ trình duyệt hạng mục'],
    ['BOM tổng hợp cấp giải pháp', 'BOM gộp các BOM tổng hợp hạng mục đã duyệt (hoặc các BOM thành phần nếu giải pháp không chia hạng mục), được gửi duyệt theo hồ sơ trình duyệt giải pháp và dùng để lập báo giá'],
    ['Hồ sơ trình duyệt', 'Hồ sơ gửi duyệt hạng mục / giải pháp, tự gắn kèm BOM tổng hợp đang ở trạng thái Hoàn thành'],
    ['Đang tạo', 'BOM mới lưu nháp, chưa gộp hay gửi duyệt được'],
    ['Hoàn thành', 'BOM đã lưu đầy đủ, sẵn sàng để gộp hoặc gửi duyệt'],
    ['Đã được tổng hợp', 'BOM thành phần đã được gộp vào một BOM tổng hợp'],
    ['Chờ duyệt', 'BOM tổng hợp đang nằm trong hồ sơ trình duyệt chờ phê duyệt'],
    ['Đã duyệt', 'BOM tổng hợp đã được phê duyệt, không sửa / xóa được nữa'],
    ['Không duyệt', 'BOM tổng hợp bị từ chối cùng hồ sơ trình duyệt'],
], widths=[2.0, 4.5])
w.h2('2. Cập nhật tài liệu')
w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung'],
         ['1.0', '02/10/2026', 'Đội phát triển phần mềm', 'Tạo mới tài liệu']], widths=[0.9, 1.1, 1.5, 3.0])
w.h2('3. Quyền sử dụng')
w.table([
    ['Bước quy trình', 'Người thực hiện / quyền cần có'],
    ['Xem danh sách BOM', 'Quyền "Xem danh sách BOM List theo tổng công ty / công ty / phòng ban / bộ phận"'],
    ['Tạo BOM thành phần, BOM tổng hợp, sao chép BOM (PHẦN 1, 2, 6, 7)', 'Quyền "Tạo BOM List"; là PM, leader hoặc thành viên của giải pháp / hạng mục'],
    ['Gửi duyệt BOM cấp hạng mục (PHẦN 3)', 'Leader phụ trách hạng mục; hạng mục ở trạng thái Đang triển khai'],
    ['Duyệt / Từ chối BOM cấp hạng mục (PHẦN 4, 5)', 'PM phụ trách giải pháp'],
    ['Gửi duyệt BOM cấp giải pháp (PHẦN 8)', 'PM phụ trách giải pháp; giải pháp ở trạng thái Đang triển khai'],
    ['Duyệt / Từ chối BOM cấp giải pháp (PHẦN 9)', 'Người tạo giải pháp (trưởng phòng giải pháp)'],
    ['Vào màn Quản lý giải pháp / Hạng mục giải pháp', 'Quyền "Xem danh sách làm giải pháp theo …" / "Xem danh sách hạng mục dự án theo …"'],
], widths=[2.6, 3.9])
w.h2('4. Sơ đồ quy trình')
w.image(os.path.join(SHOTS, '00_so_do.png'), width=6.3, caption='Sơ đồ quy trình phê duyệt BOM list')
anh_lien_chu_thich(w)

# ------------------------------------------------------------------ PHẦN 1
phan('TẠO BOM THÀNH PHẦN')
vao_bom(1)
step(['Bước 2: Bấm ', ic('btn_tao_moi_bom')])
step('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Tên BOM LIST, Dự án (Giải pháp, Khách hàng tự điền), '
     'Hạng mục nếu giải pháp có chia hạng mục.')
step(['Bước 4: Chọn Loại BOM LIST là BOM LIST thành phần ', ic('o_loai_bom')])
step(['Bước 5: Bấm ', ic('btn_them_moi_hang'), ' ở dòng A — Hàng hoá, tích chọn hàng hoá, bấm ',
      ic('btn_them_n_hang'), ' rồi bấm ', ic('btn_dong_popup_hang')])
img('10_tao_bom_tp', 'Màn hình Tạo BOM List – BOM thành phần')
sub('Hoặc xem tài liệu HDSD BOM List để nhập nhóm hàng, hàng tạm, dịch vụ, Import Excel.')
step(['Bước 6: Bấm ', ic('btn_luu_bom'), ', BOM chuyển trạng thái Hoàn thành'])
sub(['Hoặc ', ic('btn_luu_nhap'), ' để lưu ở trạng thái Đang tạo (chưa gộp, chưa gửi duyệt được).'])

# ------------------------------------------------------------------ PHẦN 2
phan('TẠO BOM TỔNG HỢP CẤP HẠNG MỤC')
vao_bom(1)
step(['Bước 2: Bấm ', ic('btn_tao_moi_bom')])
step('Bước 3: Nhập Tên BOM LIST, chọn Dự án và Hạng mục.')
step('Bước 4: Chọn Loại BOM LIST là BOM LIST tổng hợp.')
step(['Bước 5: Bấm ', ic('btn_chon_bl_con'), ', hệ thống mở cửa sổ "Chọn BOM con để gộp"'])
img('20_chon_bl_con_hm', 'Cửa sổ Chọn BOM con để gộp – cấp hạng mục')
step(['Bước 6: Tích chọn các BOM thành phần của hạng mục, bấm ', ic('btn_gop_bom_con')])
step(['Bước 7: Bấm ', ic('btn_luu_bom'), ', BOM tổng hợp chuyển Hoàn thành, các BOM thành phần đã chọn chuyển '
      'Đã được tổng hợp'])

# ------------------------------------------------------------------ PHẦN 3
phan('GỬI DUYỆT BOM CẤP HẠNG MỤC')
step(['Bước 1: '] + MENU + ['Hạng mục giải pháp ', ic('item_hang_muc_gp')])
step(['Bước 2: Bấm vào mã hạng mục ', ic('link_ma_hang_muc'), ' để mở màn quản lý hạng mục'])
step(['Bước 3: Bấm ', ic('btn_tao_hstd_hm'), ', hệ thống mở cửa sổ "Tạo hồ sơ trình duyệt"'])
img('31_hm_hoso_tao', 'Cửa sổ Tạo hồ sơ trình duyệt hạng mục')
step('Bước 4: Nhập đầy đủ thông tin bắt buộc: Tên hồ sơ, Nội dung trình duyệt, Hạn duyệt; kiểm tra BOM ở mục '
     'BOM tổng hợp gắn vào hồ sơ.')
step(['Bước 5: Bấm ', ic('btn_luu_trinh_duyet'), ', BOM tổng hợp hạng mục chuyển Chờ duyệt'])
sub(['Hoặc ', ic('btn_luu_hoso'), ' để lưu nháp hồ sơ, chưa gửi duyệt.'])
sub(['Hoặc ', ic('btn_dong_hoso'), ' để không lưu thông tin.'])

# ------------------------------------------------------------------ PHẦN 4
phan('DUYỆT BOM CẤP HẠNG MỤC')
vao_gp(1)
step(['Bước 3: Chọn thẻ ', ic('tab_hoso')])
step(['Bước 4: Bấm ', ic('btn_duyet_row'), ' (Duyệt) ở dòng hồ sơ hạng mục đang Chờ duyệt, hệ thống mở cửa sổ '
      '"Duyệt hồ sơ trình duyệt"'])
sub(['Hoặc bấm ', ic('btn_xem_row'), ' để chỉ xem hồ sơ.'])
img('34_hm_duyet_popup', 'Cửa sổ Duyệt hồ sơ trình duyệt hạng mục')
step(['Bước 5: Bấm ', ic('btn_duyet'), ', BOM tổng hợp hạng mục chuyển Đã duyệt'])
sub(['Hoặc ', ic('btn_dong_hoso'), ' để đóng cửa sổ.'])

# ------------------------------------------------------------------ PHẦN 5
phan('TỪ CHỐI BOM CẤP HẠNG MỤC')
step('Bước 1: Thực hiện Bước 1 – 4 của PHẦN 4.')
step(['Bước 2: Bấm ', ic('btn_tu_choi'), ', hệ thống mở cửa sổ "Từ chối hồ sơ"'])
img('35_hm_tu_choi', 'Cửa sổ Từ chối hồ sơ')
step('Bước 3: Nhập Lý do từ chối.')
step(['Bước 4: Bấm ', ic('btn_dong_y'), ', BOM tổng hợp hạng mục chuyển Không duyệt'])
sub(['Hoặc ', ic('btn_khong'), ' nếu bấm nhầm.'])

# ------------------------------------------------------------------ PHẦN 6
phan('ĐIỀU CHỈNH BOM BỊ TỪ CHỐI VÀ GỬI DUYỆT LẠI')
step(['Bước 1: Tại màn quản lý hạng mục, chọn thẻ ', ic('tab_hoso'), ', bấm ', ic('btn_xem_row'),
      ' ở hồ sơ Không duyệt để xem lý do từ chối'])
step(['Bước 2: Truy cập màn hình BOM Giải pháp, bấm mã BOM ', ic('link_ma_bom'),
      ' đang Không duyệt để mở chi tiết'])
step(['Bước 3: Bấm ', ic('btn_sao_chep'), ', hệ thống mở màn hình "Sao chép BOM List"'])
img('37_saochep_form', 'Màn hình Sao chép BOM List')
step('Bước 4: Sửa Tên BOM LIST, bổ sung/ sửa hàng hoá theo lý do từ chối.')
step(['Bước 5: Bấm ', ic('btn_luu_bom'), ', BOM mới chuyển Hoàn thành'])
step(['Bước 6: Leader hạng mục bấm lại ', ic('btn_tao_hstd_hm'), ' và gửi duyệt như PHẦN 3'])

# ------------------------------------------------------------------ PHẦN 7
phan('TẠO BOM TỔNG HỢP CẤP GIẢI PHÁP')
vao_bom(1)
step(['Bước 2: Bấm ', ic('btn_tao_moi_bom')])
step('Bước 3: Nhập Tên BOM LIST, chọn Dự án, để trống Hạng mục (Loại BOM LIST tự là BOM LIST tổng hợp).')
step(['Bước 4: Bấm ', ic('btn_chon_bl_con'), ', hệ thống mở cửa sổ "Chọn BOM con để gộp"'])
img('40_chon_bl_con_gp', 'Cửa sổ Chọn BOM con để gộp – cấp giải pháp')
step(['Bước 5: Tích chọn các BOM tổng hợp hạng mục Đã duyệt, bấm ', ic('btn_gop_bom_con')])
sub('Hoặc tích chọn các BOM thành phần nếu giải pháp không chia hạng mục.')
step(['Bước 6: Bấm ', ic('btn_luu_bom'), ', BOM tổng hợp cấp giải pháp chuyển Hoàn thành'])

# ------------------------------------------------------------------ PHẦN 8
phan('GỬI DUYỆT BOM CẤP GIẢI PHÁP')
vao_gp(1)
step(['Bước 3: Bấm ', ic('btn_tao_hstd_gp'), ', hệ thống mở cửa sổ "Tạo hồ sơ trình duyệt"'])
img('43_gp_hoso_tao', 'Cửa sổ Tạo hồ sơ trình duyệt giải pháp')
step('Bước 4: Nhập đầy đủ thông tin bắt buộc: Tên hồ sơ, Nội dung trình duyệt, Hạn duyệt; kiểm tra BOM ở mục '
     'BOM tổng hợp gắn vào hồ sơ.')
step(['Bước 5: Bấm ', ic('btn_luu_trinh_duyet'), ', BOM tổng hợp cấp giải pháp chuyển Chờ duyệt'])
sub('Hoặc với dự án tự triển khai, bấm Lưu & Duyệt để duyệt ngay, BOM chuyển Đã duyệt.')
sub(['Hoặc ', ic('btn_luu_hoso'), ' để lưu nháp hồ sơ, chưa gửi duyệt.'])
sub(['Hoặc ', ic('btn_dong_hoso'), ' để không lưu thông tin.'])

# ------------------------------------------------------------------ PHẦN 9
phan('DUYỆT / TỪ CHỐI BOM CẤP GIẢI PHÁP')
w.h2('1. Duyệt')
vao_gp(1)
step(['Bước 3: Chọn thẻ ', ic('tab_hoso')])
step(['Bước 4: Bấm ', ic('btn_duyet_row'), ' (Duyệt) ở dòng hồ sơ giải pháp đang Chờ duyệt, hệ thống mở cửa sổ '
      '"Duyệt hồ sơ trình duyệt"'])
img('45_gp_duyet_popup', 'Cửa sổ Duyệt hồ sơ trình duyệt giải pháp')
step(['Bước 5: Bấm ', ic('btn_duyet'), ', BOM tổng hợp cấp giải pháp chuyển Đã duyệt'])
sub(['Hoặc ', ic('btn_dong_hoso'), ' để đóng cửa sổ.'])
w.h2('2. Từ chối')
step('Bước 1: Thực hiện Bước 1 – 4 của mục 1.')
step(['Bước 2: Bấm ', ic('btn_tu_choi'), ', nhập Lý do từ chối'])
step(['Bước 3: Bấm ', ic('btn_dong_y'), ', BOM tổng hợp cấp giải pháp chuyển Không duyệt'])
sub(['Hoặc ', ic('btn_khong'), ' nếu bấm nhầm.'])
step('Bước 4: Điều chỉnh BOM như PHẦN 6 rồi PM gửi duyệt lại như PHẦN 8.')

# ------------------------------------------------------------------ PHẦN 10
phan('THEO DÕI BOM SAU KHI DUYỆT')
step('Bước 1: Truy cập màn hình BOM Giải pháp.')
step(['Bước 2: Bấm mã BOM ', ic('link_ma_bom'), ' để mở chi tiết, trạng thái hiện ở góc trên bên trái'])
img('50_bom_da_duyet', 'Màn hình Chi tiết BOM List – Đã duyệt')
step(['Bước 3: Bấm ', ic('btn_xem_lich_su'), ' ở mục Lịch sử để xem các lần Gửi duyệt, Duyệt, Không duyệt'])
step('Bước 4: Khi lập báo giá cho dự án, chọn BOM tổng hợp cấp giải pháp Đã duyệt (xem tài liệu HDSD Báo giá).')

w.rebuild_toc(levels=(1, 2))
w.save(OUT)
strip_embedded_fonts(OUT)
print(OUT)
