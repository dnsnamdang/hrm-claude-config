# -*- coding: utf-8 -*-
"""HDSD Quy trình quản lý giải pháp luồng sale tự làm (dự án TKT Tự triển khai) — khuôn GỌN."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/_catalog_docs_lib'
sys.path.insert(0, LIB)
from qg_writer import QgWriter  # noqa: E402
from hdsd_gon import h1_trang_moi, anh_lien_chu_thich, TPL, ROLES  # noqa: E402

OUT = os.path.join(HERE, 'HDSD_QuyTrinh_GiaiPhap_SaleTuLam.docx')
SH = os.path.join(HERE, 'shots')
IC = os.path.join(HERE, 'icons')

w = QgWriter(TPL, ROLES, body_from=19,
             cover_replace={'Màn hình: Danh mục khu vực': 'Quy trình quản lý giải pháp luồng sale tự làm'})


def ic(n):
    p = os.path.join(IC, n + '.png')
    assert os.path.exists(p), p
    return ('img', p)


step = w.step


def sub(segs):
    w.raw('sub', segs)


def img(name, cap, path=None):
    w.image(path or os.path.join(SH, name + '.png'), caption=cap)
    anh_lien_chu_thich(w)


n = [0]


def phan(t):
    n[0] += 1
    h1_trang_moi(w, 'PHẦN %d: %s' % (n[0], t))


VAO_DA = ['Bước 1: Từ phân hệ CSKH TRƯỚC BÁN ', ic('menu_cskh'), ', chọn menu Dự án TKT ', ic('menu_duantkt')]

# ------------------------------------------------------------------ TỔNG QUAN
h1_trang_moi(w, 'TỔNG QUAN')
w.h2('1. Thuật ngữ sử dụng trong tài liệu')
w.table([['Thuật ngữ', 'Giải thích'],
         ['Dự án TKT', 'Dự án tiền khả thi do nhân viên kinh doanh tạo cho khách hàng.'],
         ['Luồng sale tự làm', 'Dự án TKT có Cách triển khai dự án là "Tự triển khai": nhân viên kinh doanh tự làm '
          'giải pháp, không qua Yêu cầu làm giải pháp.'],
         ['NVKD chính', 'Nhân viên KD chính của dự án TKT.'],
         ['GP', 'Giải pháp.'],
         ['PM làm giải pháp', 'Người phụ trách giải pháp. Luồng sale tự làm: hệ thống tự gán người tạo giải pháp.'],
         ['Hồ sơ trình duyệt giải pháp', 'Hồ sơ gồm nội dung trình duyệt, tài liệu đính kèm và BOM tổng hợp của giải pháp.'],
         ['BOM tổng hợp', 'Danh sách hàng hóa của giải pháp, dùng để tạo báo giá.'],
         ['Trạng thái dự án', 'Thu thập thông tin dự án → Đang làm giải pháp → Trao đổi giải pháp với khách hàng → Lập dự toán.'],
         ['Trạng thái giải pháp', 'Nháp → Đang triển khai → Đã duyệt giải pháp → Chờ làm giá → Chốt giải pháp.'],
         ['Trạng thái hồ sơ', 'Nháp → Đã duyệt → Đã chốt.'],
         ], widths=[2.0, 4.5])
w.h2('2. Cập nhật tài liệu')
w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung'],
         ['1.0', '02/10/2026', 'Đội phát triển phần mềm',
          'Tạo mới tài liệu quy trình quản lý giải pháp luồng sale tự làm.']],
        widths=[0.9, 1.1, 1.5, 3.0])
w.h2('3. Quyền sử dụng')
w.table([['Bước quy trình', 'Người thực hiện / quyền cần có'],
         ['Tạo dự án TKT', 'Người dùng vào được menu Dự án TKT. Danh sách dự án hiển thị theo quyền "Xem danh sách dự án '
          'tiền khả thi theo tổng công ty / công ty / phòng ban / bộ phận".'],
         ['Tạo giải pháp', 'Người xem được dự án. Nút chỉ hiện khi dự án Tự triển khai, đang ở trạng thái Thu thập thông '
          'tin dự án, có làm GP, chưa có giải pháp và phiếu thu thập thông tin đã nhập đủ. Người tạo trở thành PM.'],
         ['Thực hiện giải pháp', 'PM làm giải pháp và nhân sự được phân công. Danh sách giải pháp hiển thị theo quyền '
          '"Xem danh sách làm giải pháp theo tổng công ty / công ty / phòng ban / bộ phận".'],
         ['Tạo hồ sơ trình duyệt và duyệt', 'PM làm giải pháp, khi giải pháp đang ở trạng thái Đang triển khai.'],
         ['Tạo báo giá từ hồ sơ', 'NVKD chính của dự án, với hồ sơ Đã duyệt có BOM tổng hợp.'],
         ['Chốt giải pháp', 'NVKD chính của dự án, khi dự án có hồ sơ Đã duyệt.'],
         ['Dự án không làm giải pháp', 'NVKD chính của dự án (tạo báo giá ở thẻ Báo giá).'],
         ], widths=[2.0, 4.5])
w.h2('4. Sơ đồ quy trình')
img(None, 'Sơ đồ quy trình quản lý giải pháp luồng sale tự làm', path=os.path.join(HERE, 'uml', 'flow.png'))

# ------------------------------------------------------------------ PHẦN 1
phan('TẠO DỰ ÁN TKT TỰ TRIỂN KHAI')
step(VAO_DA)
step(['Bước 2: Bấm ', ic('btn_taomoi')])
step('Bước 3: Nhập/ chọn đầy đủ các trường có dấu * của dự án (Khách hàng, Người liên hệ, Tên dự án TKT, Ứng dụng, '
     'Nhóm ngành, Quy mô dự án, Phân loại đầu tư, Địa điểm triển khai, Giai đoạn dự án KH, Mức độ ưu tiên giải pháp, '
     'Nhân viên KD chính, Phòng KD phụ trách chính, Loại tiền tệ, Ngân sách dự kiến…) theo HDSD Dự án TKT.')
step(['Bước 4: Tại ô Cách triển khai dự án, chọn ', ic('o_cachtrienkhai')])
img('02_add', 'Màn hình Tạo mới dự án tiền khả thi')
step(['Bước 5: Tại mục Có cần làm GP?, chọn ', ic('radio_co'), ' để đi luồng làm giải pháp (PHẦN 2 đến PHẦN 6)'])
sub(['Hoặc chọn ', ic('radio_khong'), ' nếu dự án không làm giải pháp (xem PHẦN 7).'])
step(['Bước 6: Bấm ', ic('btn_luu'), ', dự án chuyển sang trạng thái Thu thập thông tin dự án'])
sub(['Hoặc ', ic('btn_luunhap'), ' để lưu dự án ở trạng thái Đang tạo (chưa tạo được giải pháp).'])
sub(['Hoặc ', ic('btn_quaylai'), ' để không lưu.'])
step(['Bước 7: Nếu dự án có phiếu thu thập thông tin: bấm vào mã dự án ở danh sách, chọn thẻ ', ic('tab_thuthap_duan'),
      ', nhập đủ các câu bắt buộc rồi bấm ', ic('btn_luuphieu')])

# ------------------------------------------------------------------ PHẦN 2
phan('TẠO GIẢI PHÁP')
step(VAO_DA)
step(['Bước 2: Nhập mã hoặc tên dự án vào ô tìm kiếm nhanh, bấm ', ic('btn_timkiem')])
step(['Bước 3: Bấm Tạo giải pháp ', ic('btn_taogp_row'), ' ở cột Hành động của dự án'])
img('04_sol_add', 'Màn hình Tạo giải pháp')
step('Bước 4: Nhập/ chọn đầy đủ thông tin bắt buộc: Tên GP, Ngày cần xong GP, Nhóm ngành, Nhóm giải pháp. '
     'PM làm giải pháp do hệ thống tự gán là người tạo.')
step(['Bước 5: Bấm ', ic('btn_themnhansu'), ', chọn Phòng ban, Nhân sự, Vai trò dự án, Ngày bắt đầu cho từng dòng'])
step(['Bước 6: Bấm ', ic('btn_luuvagui'), ', giải pháp chuyển sang trạng thái Đang triển khai'])
sub(['Hoặc ', ic('btn_luunhap_gp'), ' để lưu Nháp, sau đó bấm Sửa ', ic('btn_sua_row'),
     ' ở danh sách Quản lý giải pháp để gửi tiếp.'])
sub(['Hoặc ', ic('btn_quaylai'), ' để không lưu.'])

# ------------------------------------------------------------------ PHẦN 3
phan('THỰC HIỆN GIẢI PHÁP')
step(['Bước 1: Từ phân hệ CÔNG VIỆC ', ic('menu_congviec'), ', tại menu ', ic('menu_lamgp'), ', chọn ',
      ic('item_quanlygp')])
step(['Bước 2: Tìm giải pháp, bấm Quản lý giải pháp ', ic('btn_quanlygp_row'), ' ở cột Hành động'])
img('06_sol_mgr', 'Màn hình Quản lý giải pháp')
step(['Bước 3: Xem nhân sự đã phân công ở thẻ ', ic('tab_nhansu')])
step(['Bước 4: Giao nhiệm vụ ở thẻ ', ic('tab_nhiemvu'), ' — thao tác theo HDSD Nhiệm vụ'])
sub(['Hoặc từ phân hệ CÔNG VIỆC, menu ', ic('menu_nhiemvu'), ', chọn ', ic('item_nhiemvu'), '.'])
step(['Bước 5: Ghi nhận, xử lý vấn đề ở thẻ ', ic('tab_vande'), ' — thao tác theo HDSD Vấn đề'])
sub(['Hoặc từ phân hệ CÔNG VIỆC, menu ', ic('menu_nhiemvu'), ', chọn ', ic('item_vande'), '.'])
step(['Bước 6: Lập BOM tổng hợp cho giải pháp: tại menu ', ic('menu_lamgp'), ', chọn ', ic('item_bomgp'),
      ', chuyển BOM sang Hoàn thành — thao tác theo HDSD BOM giải pháp'])
sub('Hoặc bỏ qua bước này nếu không lập BOM (khi đó hồ sơ trình duyệt bắt buộc có tài liệu đính kèm).')

# ------------------------------------------------------------------ PHẦN 4
phan('TẠO HỒ SƠ TRÌNH DUYỆT VÀ DUYỆT GIẢI PHÁP')
step('Bước 1: Mở màn hình Quản lý giải pháp (PHẦN 3, Bước 1–2).')
step(['Bước 2: Bấm ', ic('btn_taohoso')])
sub('Hoặc bấm Sửa hồ sơ trình duyệt giải pháp nếu đã lưu hồ sơ trước đó.')
img('07_hoso', 'Cửa sổ Tạo hồ sơ trình duyệt')
step('Bước 3: Nhập Tên hồ sơ, Nội dung trình duyệt.')
step('Bước 4: Kiểm tra mục BOM tổng hợp gắn vào hồ sơ: BOM tổng hợp Hoàn thành được tự gắn vào hồ sơ.')
sub(['Hoặc nếu hiện cảnh báo chưa có BOM: bấm ', ic('btn_themfile'), ', nhập Tên tài liệu, bấm ', ic('btn_chonfile'),
     ' để đính kèm ít nhất 1 tài liệu.'])
step(['Bước 5: Bấm ', ic('btn_luuduyet'), ', hồ sơ được duyệt ngay, giải pháp chuyển sang Đã duyệt giải pháp'])
sub(['Hoặc ', ic('btn_luu_hoso'), ' để lưu hồ sơ, trình duyệt sau.'])
sub(['Hoặc ', ic('btn_dong_hoso'), ' để không lưu.'])

# ------------------------------------------------------------------ PHẦN 5
phan('TẠO BÁO GIÁ TỪ HỒ SƠ ĐÃ DUYỆT')
step(VAO_DA + [', bấm vào mã dự án để mở dự án'])
step(['Bước 2: Chọn thẻ ', ic('tab_hoso_duan')])
img('08_hoso_duan', 'Thẻ Hồ sơ của dự án')
step(['Bước 3: Rê chuột vào mã hồ sơ Đã duyệt, bấm Tạo báo giá ', ic('btn_taobaogia_row'),
      ', hệ thống tạo báo giá từ BOM của hồ sơ và mở màn hình Làm giá'])
sub(['Hoặc bấm ', ic('btn_xemhoso_row'), ' để xem lại hồ sơ.'])
step('Bước 4: Hoàn thiện và gửi duyệt báo giá — thao tác theo HDSD Báo giá.')

# ------------------------------------------------------------------ PHẦN 6
phan('CHỐT GIẢI PHÁP')
step(VAO_DA + [', bấm vào mã dự án để mở dự án'])
step(['Bước 2: Bấm ', ic('btn_chotgp'), ' ở chân màn hình'])
img('10_chotgp', 'Cửa sổ Chốt giải pháp')
step('Bước 3: Chọn hồ sơ giải pháp, nhập Ghi chú chốt giải pháp.')
step(['Bước 4: Tại mục File xác nhận của khách hàng, bấm ', ic('btn_themfile'), ', nhập Tên tài liệu, bấm ',
      ic('btn_chonfile'), ' để đính kèm file'])
step(['Bước 5: Bấm ', ic('btn_luuguitb'), ', giải pháp chuyển sang Chốt giải pháp'])
sub(['Hoặc ', ic('btn_dong_chot'), ' để không chốt.'])

# ------------------------------------------------------------------ PHẦN 7
phan('DỰ ÁN TỰ TRIỂN KHAI KHÔNG LÀM GIẢI PHÁP')
step(['Bước 1: Khi tạo dự án (PHẦN 1), tại mục Có cần làm GP? chọn ', ic('radio_khong'), ', bấm ', ic('btn_luu')])
step(['Bước 2: Ở danh sách Dự án TKT ', ic('menu_duantkt'), ', bấm vào mã dự án để mở dự án'])
step(['Bước 3: Chọn thẻ ', ic('tab_baogia_duan')])
img('11_khonggp_baogia', 'Thẻ Báo giá của dự án không làm giải pháp')
step(['Bước 4: Bấm ', ic('btn_taobaogia'), ' để lập báo giá — thao tác theo HDSD Báo giá'])

w.rebuild_toc(levels=(1, 2))
w.save(OUT)
print(OUT)
