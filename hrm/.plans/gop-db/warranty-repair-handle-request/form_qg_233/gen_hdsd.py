# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Phiếu xử lý yêu cầu (STT 233, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Phieu xu ly yeu cau.docx (+ .pdf, render/ để soát)
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py · ảnh: capture.js (dev 28/10/2026)
Dựng lại toàn bộ nên mục lục cũ lệch thân bài của bản Drive tự hết.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Phiếu xử lý yêu cầu'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_Phieu xu ly yeu cau.docx')  # tên file Drive gốc

THUAT_NGU = [
    ['Phiếu xử lý', 'Chứng từ thứ hai của luồng dịch vụ, lập từ phiếu yêu cầu kiểm tra sửa chữa - bảo hành.'],
    ['Phiếu yêu cầu gốc', 'Phiếu yêu cầu kiểm tra sửa chữa - bảo hành mà phiếu xử lý được tạo từ đó.'],
    ['CCTT', 'Cung cấp thông tin làm báo giá — chứng từ thứ ba của luồng dịch vụ.'],
    ['Nguyên nhân', 'Công việc hoặc lỗi thiết bị lấy từ danh mục công việc – lỗi thiết bị, khai riêng cho từng hàng hóa.'],
    ['Hành động', 'Hướng xử lý từng thiết bị: Tư vấn điện thoại, hoặc Cung cấp thông tin làm báo giá.'],
    ['Hàng hóa tương đương', 'Hàng hóa trong danh mục được chọn thay cho thiết bị khách khai tự do.'],
    ['Trạng thái Đang tạo', 'Phiếu nháp hoặc bị Không duyệt trả về. Người tạo được sửa, xóa.'],
    ['Trạng thái Chờ CCTT', 'Đã gửi, chờ lập phiếu cung cấp thông tin làm báo giá.'],
    ['Trạng thái Đang CCTT / Đã CCTT', 'Phiếu cung cấp thông tin đang lập / đã gửi làm báo giá.'],
    ['Trạng thái Đã tư vấn điện thoại', 'Mọi thiết bị chọn Tư vấn điện thoại — luồng dịch vụ kết thúc.'],
]

PHIEN_BAN = [
    ['1.0', '03/09/2026', 'Biên soạn lần đầu theo phiên bản màn hình trên hệ thống HRM.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel',
     'Một trong các quyền: Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty / theo công ty '
     '/ theo phòng ban. Phiếu do chính mình tạo luôn xem được.'],
    ['Tạo phiếu xử lý', 'Quyền Xử lý yêu cầu sửa chữa, thuộc phòng tiếp nhận của phiếu yêu cầu gốc.'],
    ['Sửa, xóa phiếu', 'Người tạo phiếu, phiếu đang ở trạng thái Đang tạo.'],
    ['Thêm nhanh lỗi thiết bị', 'Quyền Quản lý danh mục công việc - lỗi thiết bị.'],
    ['Tạo phiếu cung cấp thông tin, Không duyệt', 'Quyền Tạo phiếu cung cấp thông tin, phiếu đang ở trạng thái Chờ CCTT.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('CSKH sau bán', 'menu_phanhe'), ('Kiểm tra bảo hành sửa chữa', 'menu_nhom'),
              ('Phiếu xử lý yêu cầu', 'menu_muc')],
        o_nhanh='số phiếu xử lý, số phiếu yêu cầu, tên khách hàng hoặc người xử lý',
        bo_loc=[('Trạng thái', 'o_trangthai'), ('Số phiếu yêu cầu', 'o_sophieuyc'), ('Khách hàng', 'o_khachhang'),
                ('Tên thiết bị', 'o_tenthietbi'), ('Model', 'o_model'), ('Ngày tạo', 'o_ngaytao')])

    # PHẦN 2 — Tạo phiếu
    d.phan('TẠO PHIẾU XỬ LÝ')
    d.step('Bước 1: Truy cập màn hình Yêu cầu kiểm tra sửa chữa - bảo hành, mở phiếu Chờ xử lý gửi về phòng mình.')
    d.step(['Bước 2: Bấm ', '@btn_xuly', '. Hệ thống mở màn “Lập phiếu xử lý yêu cầu”, chép sẵn khách hàng và thiết bị.'])
    d.img('10_create', 'Màn hình Lập phiếu xử lý yêu cầu')
    d.step('Bước 3: Nhập thông tin từng thiết bị:')
    d.sub('Nguyên nhân: chọn một hoặc nhiều nguyên nhân (bắt buộc khi Lưu và gửi; không chọn trùng).')
    d.sub(['Hoặc bấm ', '@btn_themnhanh', ' để khai nhanh nguyên nhân mới (cần quyền Quản lý danh mục công việc - '
           'lỗi thiết bị).'])
    d.sub(['Hành động ', '@o_hanhdong', ': chọn Tư vấn điện thoại hoặc Cung cấp thông tin làm báo giá (bắt buộc khi '
           'Lưu và gửi).'])
    d.sub('Nội dung xử lý: bắt buộc khi chọn Tư vấn điện thoại, kể cả khi Lưu nháp.')
    d.sub('Chọn hàng hóa tương đương: bắt buộc với thiết bị khách khai tự do khi Lưu và gửi.')
    d.sub('File đính kèm (PDF, ảnh, Word, Excel): tùy chọn.')
    d.step(['Bước 4: Bấm ', '@btn_luugui', ', chọn ', '@btn_confirm_xacnhan', ' để gửi làm báo giá,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])
    d.sub('Mọi thiết bị chọn Tư vấn điện thoại thì phiếu và phiếu yêu cầu gốc chuyển ngay sang “Đã tư vấn điện '
          'thoại”, kể cả khi bấm Lưu nháp.')

    # PHẦN 3 — Thêm nhanh nguyên nhân
    d.phan('THÊM NHANH LỖI THIẾT BỊ')
    d.step(['Bước 1: Tại màn Lập / Sửa phiếu xử lý, bấm ', '@btn_themnhanh', ' dưới ô Nguyên nhân của dòng thiết bị.'])
    d.img('11_quickadd', 'Cửa sổ Thêm nhanh công việc / lỗi thiết bị')
    d.step('Bước 2: Nhập Loại công việc / lỗi và Tên công việc / Tình trạng lỗi (bắt buộc); các ô còn lại tùy chọn.')
    d.step(['Bước 3: Bấm ', '@btn_luu_qa', '. Nguyên nhân mới được tự chọn vào dòng thiết bị,'])
    d.sub(['Hoặc bấm ', '@btn_dong_modal', ' nếu muốn hủy.'])

    # PHẦN 4 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do mình tạo.'])
    d.sub(['Hoặc bấm vào Số phiếu xử lý để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa phiếu xử lý yêu cầu”.')
    d.img('12_edit', 'Màn hình Sửa phiếu xử lý yêu cầu')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như PHẦN 2).')
    d.step(['Bước 5: Bấm ', '@btn_luugui', ' để lưu và gửi,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 5 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Số phiếu xử lý để mở màn chi tiết, chọn ', '@btn_xoa'])
    d.sub('Phiếu yêu cầu gốc trở lại Chờ xử lý để lập lại phiếu xử lý.')

    # PHẦN 6 — Tạo phiếu CCTT
    d.phan('TẠO PHIẾU CUNG CẤP THÔNG TIN')
    d.step(['Bước 1: Bấm ', '@btn_cctt_row', ' ở cột Hành động của phiếu Chờ CCTT.'])
    d.sub(['Hoặc bấm vào Số phiếu xử lý để mở màn chi tiết, chọn ', '@btn_cctt'])
    d.img('14_wait_detail', 'Màn hình Chi tiết phiếu xử lý đang Chờ CCTT')
    d.step('Bước 2: Hệ thống mở màn lập Phiếu cung cấp thông tin làm báo giá (xem HDSD màn đó).')

    # PHẦN 7 — Không duyệt
    d.phan('KHÔNG DUYỆT PHIẾU')
    d.step(['Bước 1: Bấm ', '@btn_khongduyet_row', ' ở cột Hành động của phiếu Chờ CCTT.'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_khongduyet'])
    d.step('Bước 2: Hệ thống mở cửa sổ “Không duyệt phiếu xử lý yêu cầu”.')
    d.img('15_reject', 'Cửa sổ Không duyệt phiếu xử lý yêu cầu')
    d.step('Bước 3: Nhập Lý do không duyệt (bắt buộc). Phiếu trở về Đang tạo; phiếu yêu cầu gốc giữ nguyên.')
    d.step(['Bước 4: Bấm ', '@btn_confirm_khongduyet', ' để xác nhận'])
    d.sub(['Hoặc bấm ', '@btn_dong_reject', ' nếu muốn hủy.'])

    # PHẦN 8 — Lịch sử
    d.lich_su('Số phiếu xử lý', img='16_history', cap='Cửa sổ Lịch sử thay đổi của phiếu')

    # PHẦN 9 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Số phiếu xử lý. Hệ thống mở màn “Chi tiết phiếu xử lý yêu cầu”.')
    d.img('17_detail', 'Màn hình Chi tiết phiếu xử lý yêu cầu')
    d.step('Bước 3: Bấm Số phiếu yêu cầu để mở phiếu yêu cầu gốc.')
    d.step(['Bước 4: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 10 — In
    d.phan('IN PHIẾU VÀ IN DANH SÁCH')
    d.h2('1. In phiếu')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu xử lý yêu cầu')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])
    d.h2('2. In danh sách')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1), tối đa 2.000 dòng.')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách phiếu xử lý yêu cầu')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])

    d.xuat_excel(cua_so='Chọn trường xuất file')
    d.cai_dat_bo_loc()
    d.tuy_chinh_cot()
    return d.save(OUT)


if __name__ == '__main__':
    out = build()
    pdf = os.path.splitext(out)[0] + '.pdf'
    size = finalize_word(out, pdf)
    print('docx', out, size)
    print('TOC:')
    for line in toc_lines(out):
        print('  ', line)
    n, warn, sheets = render_check(pdf, os.path.join(HERE, 'out', 'render'))
    print('pages', n)
    for w_ in warn:
        print('WARN', w_)
    for s in sheets:
        print(s)
