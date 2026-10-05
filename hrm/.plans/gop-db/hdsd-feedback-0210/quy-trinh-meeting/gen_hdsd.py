# -*- coding: utf-8 -*-
"""HDSD Quy trình vòng đời meeting — bản GỌN (skill hdsd-documenter, khuôn HDSD_MAU_GON.docx).

Chạy: /opt/homebrew/bin/python3 gen_hdsd.py
Ảnh ở shots/ (chụp thật cuộc họp demo TPE.MET.NB.26.0067), icon ở icons/ rồi tới catalog-docs-v2/icons.
Mục lục: rebuild_toc dựng sẵn dòng, số trang để Word cập nhật (user làm bước cuối).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, '..', '..', '_catalog_docs_lib')
sys.path.insert(0, LIB)
from qg_writer import QgWriter  # noqa: E402
from hdsd_gon import h1_trang_moi, anh_lien_chu_thich, TPL, ROLES, SHARED_ICONS  # noqa: E402

OUT = os.path.join(HERE, 'HDSD_QuyTrinh_VongDoiMeeting.docx')


def ic(name):
    for d in (os.path.join(HERE, 'icons'), SHARED_ICONS):
        p = os.path.join(d, name + '.png')
        if os.path.exists(p):
            return ('img', p)
    raise AssertionError('Thiếu icon ' + name)


w = QgWriter(TPL, ROLES, body_from=19,
             cover_replace={'Màn hình: Danh mục khu vực': 'Quy trình vòng đời meeting',
                            'Danh mục khu vực': 'Quy trình vòng đời meeting'})
step = w.step


def sub(segs):
    w.raw('sub', segs)


def img(name, cap):
    w.image(os.path.join(HERE, 'shots', name + '.png'), caption=cap)
    anh_lien_chu_thich(w)


n = [0]


def phan(title):
    n[0] += 1
    h1_trang_moi(w, 'PHẦN %d: %s' % (n[0], title))


# ------------------------------------------------------------------ TỔNG QUAN
h1_trang_moi(w, 'TỔNG QUAN')
w.h2('1. Thuật ngữ sử dụng trong tài liệu')
w.table([['Thuật ngữ', 'Giải thích'],
         ['Meeting (cuộc họp)', 'Một buổi họp nội bộ hoặc họp với đối tác/khách hàng, được quản lý từ lúc lên lịch tới khi có biên bản.'],
         ['Người chủ trì', 'Nhân viên chủ trì cuộc họp, mặc định là người tạo; luôn nằm trong Thành phần — Phía Công ty.'],
         ['Thành phần — Phía Công ty', 'Danh sách nhân viên nội bộ được mời họp; nhận thông báo lịch họp và tự xác nhận tham dự.'],
         ['Biên bản', 'Nội dung trao đổi, người thực hiện, hạn dự kiến, tài liệu đính kèm và kết luận của cuộc họp.'],
         ['Hạn nhập biên bản', 'Thời gian kết thúc cuộc họp cộng thêm số ngày quy định; quá hạn mà chưa Hoàn thành thì cuộc họp bị tự động Hủy.'],
         ['Trạng thái Lưu nháp', 'Cuộc họp mới soạn, chưa gửi lịch cho ai. Danh sách hiển thị là "Đang tạo".'],
         ['Trạng thái Lên lịch', 'Đã gửi lịch họp tới thành phần tham gia, chờ chốt thời gian.'],
         ['Trạng thái Chốt lịch', 'Đã chốt thời gian và địa điểm; được điểm danh và lập biên bản.'],
         ['Trạng thái Hoàn thành', 'Cuộc họp đã diễn ra và có biên bản; không sửa được nữa.'],
         ['Trạng thái Hủy', 'Cuộc họp bị hủy (kèm lý do) hoặc bị hệ thống tự hủy khi quá hạn nhập biên bản; không sửa được nữa.']],
        widths=[2.0, 4.5])
w.h2('2. Cập nhật tài liệu')
w.table([['Phiên bản', 'Ngày', 'Người cập nhật', 'Nội dung'],
         ['1.0', '02/10/2026', 'Đội phát triển phần mềm', 'Tạo mới tài liệu hướng dẫn quy trình vòng đời meeting.']],
        widths=[0.9, 1.1, 1.5, 3.0])
w.h2('3. Quyền sử dụng')
w.table([['Chức năng', 'Ai được dùng'],
         ['Truy cập, Tạo meeting', 'Mọi nhân viên đã đăng nhập.'],
         ['Xem meeting', 'Người tạo, người chủ trì, người trong Thành phần — Phía Công ty; ngoài ra người có quyền "Xem danh sách meeting theo tổng công ty / công ty / phòng ban / bộ phận".'],
         ['Sửa, Lên lịch, Chốt lịch, Điểm danh, Lập biên bản, Hoàn thành', 'Người tạo hoặc người chủ trì cuộc họp.'],
         ['Hủy, Xóa', 'Chỉ người tạo cuộc họp.'],
         ['Xác nhận tham dự', 'Nhân viên có tên trong Thành phần — Phía Công ty.'],
         ['In biên bản', 'Người xem được cuộc họp.']],
        widths=[2.3, 4.2])
w.h2('4. Sơ đồ quy trình')
w.image(os.path.join(HERE, 'uml', 'overview.png'), caption='Sơ đồ vòng đời một cuộc họp')
anh_lien_chu_thich(w)

# ------------------------------------------------------------------ PHẦN 1
phan('TRUY CẬP MÀN HÌNH TỔNG HỢP MEETING')
step(['Bước 1: Bấm ', ic('btn_phanhe'), ' trên thanh tiêu đề, chọn phân hệ ', ic('item_meeting')])
step(['Bước 2: Tại menu bên trái, chọn ', ic('menu_tonghop')])
img('01_list', 'Màn hình Danh sách meeting')

# ------------------------------------------------------------------ PHẦN 2
phan('TẠO MEETING')
step('Bước 1: Truy cập màn hình Danh sách meeting (xem PHẦN 1).')
step(['Bước 2: Bấm ', ic('btn_taomoi')])
img('02_create', 'Màn hình Tạo meeting')
step('Bước 3: Nhập/ chọn đầy đủ thông tin bắt buộc: Tên meeting, Loại meeting, Bắt đầu, Kết thúc, Người chủ trì.')
sub('Hoặc với Họp đối tác: chọn thêm Khách hàng và Người liên hệ.')
sub('Hoặc với Hình thức Trực tiếp mà chưa đăng ký phòng họp: nhập Địa điểm meeting (bắt buộc khi Chốt lịch).')
step('Bước 4: Chọn thành phần tham gia (xem PHẦN 3).')
step(['Bước 5: Bấm ', ic('btn_luunhap'), ' để lưu nháp, chưa gửi lịch họp,'])
sub(['Hoặc ', ic('btn_luulenlich'), ' để lưu và gửi lịch họp tới thành phần tham gia,'])
sub(['Hoặc ', ic('btn_luuchotlich'), ' để lưu và chốt lịch luôn,'])
sub(['Hoặc ', ic('btn_quaylai'), ' để không lưu.'])

# ------------------------------------------------------------------ PHẦN 3
phan('CHỌN THÀNH PHẦN THAM GIA')
step(['Bước 1: Tại màn hình Tạo/ Sửa meeting, ở khối Thành phần — Phía Công ty bấm ', ic('btn_plus_congty')])
step('Bước 2: Hệ thống mở cửa sổ “Chọn nhân viên phía công ty”.')
img('03_pick_staff', 'Cửa sổ Chọn nhân viên phía công ty')
step(['Bước 3: Nhập tên hoặc mã nhân viên vào ô tìm kiếm, bấm ', ic('btn_timkiem_popup')])
step('Bước 4: Tích chọn các nhân viên cần mời.')
step(['Bước 5: Bấm ', ic('btn_themthanhvien'), ' để thêm vào danh sách,'])
sub(['Hoặc ', ic('btn_dong_popup'), ' để không thêm.'])
sub('Hoặc với Họp đối tác: ở khối Thành phần — Phía Khách hàng bấm dấu + rồi nhập Họ tên, Chức vụ, SĐT người tham dự.')

# ------------------------------------------------------------------ PHẦN 4
phan('CHỈNH SỬA MEETING')
step('Bước 1: Truy cập màn hình Danh sách meeting (xem PHẦN 1).')
step(['Bước 2: Bấm ', ic('btn_sua_row'), ' ở cột Hành động,'])
sub(['Hoặc bấm vào mã meeting để mở chi tiết, rồi bấm ', ic('btn_sua_footer')])
step('Bước 3: Hệ thống hiển thị màn hình “Sửa meeting”.')
img('04_edit', 'Màn hình Sửa meeting')
step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Tạo meeting).')
step(['Bước 5: Bấm ', ic('btn_luunhap'), ' với meeting đang Lưu nháp,'])
sub(['Hoặc ', ic('btn_luu'), ' với meeting đã Lên lịch/ Chốt lịch,'])
sub(['Hoặc ', ic('btn_quaylai'), ' để không lưu.'])

# ------------------------------------------------------------------ PHẦN 5
phan('LÊN LỊCH VÀ CHỐT LỊCH')
step('Bước 1: Mở màn hình Sửa meeting đang Lưu nháp hoặc Lên lịch (xem PHẦN 4).')
img('05_schedule_edit', 'Màn hình Sửa meeting ở trạng thái Lên lịch')
step(['Bước 2: Bấm ', ic('btn_luulenlich'), ' để gửi lịch họp, meeting chuyển sang Lên lịch.'])
sub(['Hoặc ở trạng thái Lên lịch, bấm ', ic('btn_luulenlich'), ' để gửi lại thông báo lịch họp,'])
sub(['Hoặc ', ic('btn_luu'), ' để chỉ lưu thay đổi.'])
step(['Bước 3: Khi đã thống nhất thời gian, địa điểm, bấm ', ic('btn_luuchotlich'),
      ', meeting chuyển sang Chốt lịch và hệ thống gửi thông báo chốt lịch.'])

# ------------------------------------------------------------------ PHẦN 6
phan('XÁC NHẬN THAM DỰ')
step('Bước 1: Thành viên được mời bấm vào thông báo lịch họp trên chuông, hoặc bấm vào mã meeting ở màn hình Danh sách meeting.')
step('Bước 2: Hệ thống mở màn hình Chi tiết meeting, có dòng “Xác nhận tham dự”.')
img('06_confirm_attend', 'Dòng Xác nhận tham dự trên màn hình Chi tiết meeting')
step(['Bước 3: Bấm ', ic('btn_comat'), ' để xác nhận tham dự,'])
sub(['Hoặc bấm ', ic('btn_vangcolydo'), ', nhập Ghi chú/ Lý do rồi bấm ', ic('btn_xacnhan_vang')])

# ------------------------------------------------------------------ PHẦN 7
phan('ĐIỂM DANH')
step('Bước 1: Mở màn hình Sửa meeting đang Chốt lịch (xem PHẦN 4).')
step(['Bước 2: Chọn thẻ ', ic('tab_diemdanh')])
img('07_attendance', 'Thẻ Điểm danh')
step(['Bước 3: Bấm ', ic('btn_diemdanhnhanh'), ' để đánh dấu tất cả có mặt,'])
sub(['Hoặc chọn trạng thái cho từng người ', ic('chips_diemdanh', ), ' và nhập Ghi chú/ Lý do nếu vắng.'])
step(['Bước 4: Bấm ', ic('btn_luu')])

# ------------------------------------------------------------------ PHẦN 8
phan('LẬP BIÊN BẢN')
step('Bước 1: Mở màn hình Sửa meeting đang Chốt lịch (xem PHẦN 4).')
step(['Bước 2: Chọn thẻ ', ic('tab_bienban')])
img('08_report', 'Thẻ Biên bản')
step(['Bước 3: Tại mục Các nội dung khác, bấm ', ic('btn_themdong'),
      ', nhập Nội dung/ Vấn đề trao đổi, Phương án xử lý, chọn Người thực hiện ', ic('o_nguoithuchien'),
      ' (tích chọn rồi bấm ', ic('btn_themthanhvien1'), '), chọn Hạn dự kiến.'])
step(['Bước 4: Tại mục Tài liệu đính kèm, bấm ', ic('btn_themtailieu'), ', nhập Tên tài liệu, bấm ',
      ic('btn_chontep'), ' để chọn file.'])
step('Bước 5: Nhập nội dung Kết luận.')
step(['Bước 6: Bấm ', ic('btn_luu'), ' để lưu biên bản,'])
sub(['Hoặc ', ic('btn_hoanthanh'), ' để lưu và hoàn thành cuộc họp (xem PHẦN 9).'])

# ------------------------------------------------------------------ PHẦN 9
phan('HOÀN THÀNH MEETING')
step('Bước 1: Mở màn hình Sửa meeting đang Chốt lịch, đã tới giờ bắt đầu (xem PHẦN 4).')
step('Bước 2: Kiểm tra đã điểm danh đủ thành viên (PHẦN 7), đã nhập biên bản và kết luận (PHẦN 8).')
step(['Bước 3: Bấm ', ic('btn_hoanthanh'), ', meeting chuyển sang Hoàn thành.'])
sub('Hoặc nếu còn thiếu, hệ thống báo danh sách mục cần nhập và chuyển tới thẻ đang thiếu; nhập bổ sung rồi bấm lại.')
img('09_complete', 'Meeting ở trạng thái Đã hoàn thành')

# ------------------------------------------------------------------ PHẦN 10
phan('IN BIÊN BẢN')
step(['Bước 1: Mở chi tiết meeting (bấm vào mã meeting), bấm ', ic('btn_in_footer')])
sub(['Hoặc tại màn hình Danh sách meeting, bấm ', ic('btn_in_row'), ' ở cột Hành động,'])
sub(['Hoặc bấm ', ic('btn_bacham_row'), ' rồi chọn ', ic('item_inbienban')])
sub(['Hoặc trong thẻ Biên bản, bấm ', ic('btn_in_bienban')])
step('Bước 2: Hệ thống mở cửa sổ “Cấu hình in biên bản”, tích chọn các phần cần in.')
step(['Bước 3: Bấm ', ic('btn_xemtruoc')])
img('11_print_preview', 'Cửa sổ Xem trước biên bản cuộc họp')
step(['Bước 4: Bấm ', ic('btn_in_preview'), ' để in biên bản.'])

# ------------------------------------------------------------------ PHẦN 11
phan('HỦY MEETING')
step(['Bước 1: Mở chi tiết hoặc màn hình Sửa meeting đang Lên lịch/ Chốt lịch, chưa tới giờ bắt đầu, bấm ',
      ic('btn_huy_footer')])
step('Bước 2: Hệ thống mở cửa sổ “Xác nhận hủy cuộc họp”.')
img('12_cancel', 'Cửa sổ Xác nhận hủy cuộc họp')
step('Bước 3: Chọn Lý do hủy cuộc họp, nhập Ghi chú (nếu có).')
step(['Bước 4: Bấm ', ic('btn_xacnhanhuy'), ', meeting chuyển sang Hủy và hệ thống báo cho thành viên,'])
sub(['Hoặc ', ic('btn_dong_modal'), ' nếu không hủy.'])

# ------------------------------------------------------------------ PHẦN 12
phan('TỰ ĐỘNG HỦY KHI QUÁ HẠN BIÊN BẢN')
step('Bước 1: Sau giờ kết thúc, thẻ Biên bản hiển thị hạn nhập biên bản.')
img('13_deadline_banner', 'Thông báo hạn nhập biên bản trong thẻ Biên bản')
step('Bước 2: Trước hạn (mặc định 3 giờ), hệ thống gửi thông báo nhắc người tạo meeting.')
step('Bước 3: Quá hạn (mặc định 1 ngày sau giờ kết thúc) mà meeting chưa Hoàn thành, hệ thống tự chuyển sang Hủy và báo người tạo cùng thành viên nội bộ.')
sub('Số ngày hạn và số giờ cảnh báo do quản trị khai báo ở mục “Hạn nhập biên bản meeting sau” và “Cảnh báo trước khi tự hủy meeting” trong phần cài đặt.')

# ------------------------------------------------------------------ PHẦN 13
phan('XÓA MEETING')
step('Bước 1: Truy cập màn hình Danh sách meeting (xem PHẦN 1).')
step(['Bước 2: Tại meeting đang Lưu nháp, bấm ', ic('btn_xoa_row'), ' ở cột Hành động,'])
sub(['Hoặc mở chi tiết meeting rồi bấm ', ic('btn_xoa_footer')])
step('Bước 3: Hệ thống hiện hộp xác nhận “Xác nhận xóa”.')
img('14_delete', 'Hộp xác nhận xóa meeting')
step(['Bước 4: Bấm ', ic('btn_confirm_xoa'), ' để xác nhận xóa,'])
sub(['Hoặc bấm ', ic('btn_huy_confirm'), ' nếu bấm nhầm.'])

w.rebuild_toc(levels=(1, 2))
print('OK', w.save(OUT))
