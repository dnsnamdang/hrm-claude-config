# -*- coding: utf-8 -*-
"""HDSD bản GỌN — Yêu cầu kiểm tra sửa chữa - bảo hành (STT 232, form chuẩn Danh mục quốc gia, 28/10/2026).

Chạy: python gen_hdsd.py  → out/HDSD_Yeu cau kiem tra sua chua - bao hanh.docx (+ .pdf, render/ để soát)
Phần dùng chung: ../../phieu-theo-form-quoc-gia/hdsd_phieu_lib.py · ảnh: capture.js (dev 28/10/2026)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
from hdsd_phieu_lib import PhieuHdsd, finalize_word, toc_lines, render_check  # noqa: E402

TEN = 'Yêu cầu kiểm tra sửa chữa - bảo hành'
SHOTS = os.path.join(HERE, 'hdsd_shots')
OUT = os.path.join(HERE, 'out', 'HDSD_Yeu cau kiem tra sua chua - bao hanh.docx')  # tên file Drive gốc

THUAT_NGU = [
    ['Phiếu yêu cầu', 'Chứng từ mở đầu của luồng dịch vụ: ghi nhận việc khách hàng báo thiết bị cần kiểm tra, '
                      'sửa chữa hoặc bảo hành.'],
    ['Phòng tiếp nhận xử lý', 'Phòng ban nhận phiếu. Người của phòng này có quyền xử lý mới tạo phiếu xử lý, chuyển '
                              'phòng hoặc từ chối phiếu.'],
    ['Phiếu xử lý yêu cầu', 'Chứng từ tiếp theo, do phòng tiếp nhận lập từ phiếu yêu cầu.'],
    ['Lưu nháp', 'Lưu phiếu ở trạng thái Đang tạo. Chỉ người lập nhìn thấy.'],
    ['Lưu và gửi', 'Gửi phiếu cho phòng tiếp nhận. Phiếu chuyển sang Chờ xử lý và không sửa được nữa.'],
    ['Số BBBGNT / BBXNCV', 'Số biên bản bàn giao nghiệm thu hoặc biên bản xác nhận công việc đã ký với khách hàng.'],
    ['Trang thiết bị hiện có của khách hàng', 'Danh mục thiết bị khách đang sở hữu — mua của Tân Phát hoặc của nơi '
                                              'khác.'],
    ['Trạng thái Đang tạo', 'Phiếu nháp hoặc bị phòng tiếp nhận từ chối trả về. Người lập được sửa, xóa.'],
    ['Trạng thái Chờ xử lý', 'Đã gửi cho phòng tiếp nhận, đang chờ xử lý.'],
    ['Các trạng thái sau', 'Đang xử lý, Đang CCTT, Đã CCTT báo giá, Đã báo giá, Đã lập hợp đồng, Đã xử lý, Đã tư vấn '
                           'điện thoại: do các chứng từ phía sau cập nhật.'],
]

PHIEN_BAN = [
    ['1.0', '03/09/2026', 'Biên soạn lần đầu theo phiên bản màn hình trên hệ thống HRM.'],
    ['1.1', '28/10/2026', 'Chuyển sang form chuẩn'],
]

QUYEN = [
    ['Xem danh sách, xem chi tiết, in, xuất Excel',
     'Một trong các quyền: Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng công ty / theo công ty / theo phòng '
     'ban. Phiếu do chính mình lập luôn xem được.'],
    ['Lập phiếu', 'Không cần quyền riêng.'],
    ['Sửa, xóa phiếu', 'Người lập phiếu, phiếu đang ở trạng thái Đang tạo.'],
    ['Tạo phiếu xử lý yêu cầu, chuyển phòng tiếp nhận, từ chối',
     'Quyền Xử lý yêu cầu sửa chữa, thuộc phòng tiếp nhận của phiếu, phiếu Chờ xử lý và chưa có phiếu xử lý.'],
]


def build():
    d = PhieuHdsd(TEN, SHOTS)
    d.tong_quan(THUAT_NGU, PHIEN_BAN, QUYEN, os.path.join(HERE, 'uml', 'overview_srs.png'))

    # PHẦN 1
    d.truy_cap(
        menu=[('CSKH sau bán', 'menu_phanhe'), ('Kiểm tra bảo hành sửa chữa', 'menu_nhom'),
              ('Yêu cầu kiểm tra sửa chữa - bảo hành', 'menu_muc')],
        o_nhanh='mã phiếu, tên khách hàng hoặc người tạo',
        bo_loc=[('Trạng thái', 'o_trangthai'), ('Khách hàng', 'o_khachhang'), ('Tên thiết bị', 'o_tenthietbi'),
                ('Người yêu cầu', 'o_nguoiyeucau'), ('Tỉnh/TP', 'o_tinhtp'), ('Ngày yêu cầu', 'o_ngayyeucau')])

    # PHẦN 2 — Lập phiếu
    d.phan('LẬP PHIẾU YÊU CẦU')
    d.step(d.vao)
    d.step(['Bước 2: Bấm ', '@btn_taomoi'])
    d.img('10_create', 'Màn hình Tạo yêu cầu kiểm tra sửa chữa – bảo hành')
    d.step('Bước 3: Bấm vào ô Khách hàng (bắt buộc), tìm theo tên/mã, mã số thuế hoặc số điện thoại rồi chọn khách.')
    d.img('11_customer', 'Cửa sổ Chọn khách hàng')
    d.step('Bước 4: Nhập thông tin khách hàng:')
    d.sub('Người liên hệ, Địa chỉ sửa chữa: chọn trong danh sách của khách (bắt buộc khi Lưu và gửi).')
    d.sub('Ghi chú: nhập chữ, tối đa 255 ký tự (bắt buộc khi Lưu và gửi).')
    d.sub('Phòng tiếp nhận xử lý: chọn phòng sẽ xử lý phiếu (bắt buộc khi Lưu và gửi).')
    d.sub('Số điện thoại liên hệ, Loại hình tổ chức: hệ thống tự điền.')
    d.step('Bước 5: Ở bảng “Danh mục trang thiết bị hiện có của khách hàng”, bấm + ở dòng thiết bị cần kiểm tra.')
    d.sub('Hoặc bấm “Thêm trang thiết bị của khách hàng” để khai thiết bị chưa có trong danh mục.')
    d.step('Bước 6: Nhập thông tin từng thiết bị:')
    d.sub('Serial, Nội dung yêu cầu: bắt buộc khi Lưu và gửi; serial không được trùng giữa các dòng.')
    d.sub('Số BBBGNT / BBXNCV, File đính kèm (PDF, ảnh, Word, Excel; tối đa 20MB): tùy chọn.')
    d.step(['Bước 7: Bấm ', '@btn_luugui', ', chọn ', '@btn_confirm_xacnhan', ' để gửi phòng tiếp nhận,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp (chỉ cần Khách hàng và tên thiết bị).'])
    d.sub(['Hoặc ', '@btn_luutieptuc', ' để lưu nháp rồi lập tiếp phiếu khác.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' để không lưu thông tin.'])

    # PHẦN 3 — Chỉnh sửa
    d.phan('CHỈNH SỬA')
    d.step(d.vao)
    d.step(['Bước 2: Bấm nút ', '@btn_sua_row', ' ở cột Hành động của phiếu Đang tạo do mình lập.'])
    d.sub(['Hoặc bấm vào Số phiếu để mở màn chi tiết, chọn ', '@btn_sua'])
    d.step('Bước 3: Hệ thống hiển thị màn hình “Sửa yêu cầu kiểm tra sửa chữa – bảo hành”.')
    d.img('12_edit', 'Màn hình Sửa yêu cầu kiểm tra sửa chữa – bảo hành')
    d.step('Bước 4: Nhập thông tin cần sửa (quy tắc nhập như Lập phiếu ở PHẦN 2).')
    d.step(['Bước 5: Bấm ', '@btn_luugui', ' để lưu và gửi,'])
    d.sub(['Hoặc ', '@btn_luunhap', ' để lưu nháp.'])
    d.sub(['Hoặc ', '@btn_quaylai', ' nếu muốn hủy.'])

    # PHẦN 4 — Xóa
    d.xoa('Xác nhận xóa', them_cach=['Hoặc bấm vào Số phiếu để mở màn chi tiết, chọn ', '@btn_xoa'])

    # PHẦN 5 — Tạo phiếu xử lý yêu cầu
    d.phan('TẠO PHIẾU XỬ LÝ YÊU CẦU')
    d.step(['Bước 1: Bấm ', '@btn_xuly_row', ' ở cột Hành động của phiếu Chờ xử lý gửi về phòng mình.'])
    d.sub(['Hoặc bấm vào Số phiếu để mở màn chi tiết, chọn ', '@btn_xuly'])
    d.img('17_detail', 'Màn hình Chi tiết phiếu Chờ xử lý')
    d.step('Bước 2: Hệ thống mở màn Lập phiếu xử lý yêu cầu, chép sẵn khách hàng và thiết bị '
           '(xem HDSD Phiếu xử lý yêu cầu).')

    # PHẦN 6 — Chuyển phòng tiếp nhận
    d.phan('CHUYỂN PHÒNG TIẾP NHẬN')
    d.step(['Bước 1: Bấm ', '@btn_chuyenphong_row', ' ở cột Hành động của phiếu Chờ xử lý.'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_chuyenphong'])
    d.step('Bước 2: Hệ thống mở cửa sổ “Chuyển phòng tiếp nhận”.')
    d.img('14_transfer', 'Cửa sổ Chuyển phòng tiếp nhận')
    d.step('Bước 3: Chọn Phòng tiếp nhận mới (bắt buộc, khác phòng hiện tại).')
    d.step(['Bước 4: Bấm ', '@btn_confirm_chuyen', ' để chuyển phòng'])
    d.sub(['Hoặc bấm ', '@btn_dong_modal', ' nếu muốn hủy.'])

    # PHẦN 7 — Từ chối
    d.phan('TỪ CHỐI YÊU CẦU')
    d.step(['Bước 1: Bấm ', '@btn_bacham_row', ' ở cột Hành động của phiếu Chờ xử lý, chọn ', '@item_tuchoi'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_tuchoi'])
    d.step('Bước 2: Hệ thống mở cửa sổ “Từ chối yêu cầu”.')
    d.img('15_reject', 'Cửa sổ Từ chối yêu cầu')
    d.step('Bước 3: Nhập Lý do từ chối (bắt buộc). Phiếu sẽ trở về Đang tạo để người lập sửa và gửi lại.')
    d.step(['Bước 4: Bấm ', '@btn_confirm_tuchoi', ' để xác nhận'])
    d.sub(['Hoặc bấm ', '@btn_dong_modal', ' nếu muốn hủy.'])

    # PHẦN 8 — Lịch sử
    d.lich_su('Số phiếu', img='16_history', cap='Cửa sổ Lịch sử thay đổi của phiếu')

    # PHẦN 9 — Xem chi tiết
    d.phan('XEM CHI TIẾT PHIẾU')
    d.step(d.vao)
    d.step('Bước 2: Bấm vào Số phiếu. Hệ thống mở màn “Chi tiết yêu cầu kiểm tra sửa chữa – bảo hành” '
           '(Hình ở PHẦN 5).')
    d.step(['Bước 3: Bấm ', '@btn_quaylai', ' để về màn danh sách.'])

    # PHẦN 10 — In
    d.phan('IN PHIẾU VÀ IN DANH SÁCH')
    d.h2('1. In phiếu')
    d.step(['Bước 1: Ở cột Hành động, bấm ', '@btn_in_row'])
    d.sub(['Hoặc bấm ', '@btn_bacham_row', ' rồi chọn ', '@item_in'])
    d.sub(['Hoặc tại màn chi tiết phiếu, bấm ', '@btn_in'])
    d.step('Bước 2: Hệ thống mở cửa sổ xem trước bản in.')
    d.img('18_print', 'Cửa sổ Xem trước phiếu yêu cầu')
    d.step(['Bước 3: Bấm ', '@btn_in_preview', ' để in.'])
    d.h2('2. In danh sách')
    d.step('Bước 1: Lọc danh sách theo đúng dữ liệu cần in (xem PHẦN 1), tối đa 2.000 dòng.')
    d.step(['Bước 2: Bấm ', '@btn_in_list', '. Hệ thống mở cửa sổ xem trước danh sách.'])
    d.img('19_printlist', 'Cửa sổ Xem trước danh sách yêu cầu kiểm tra sửa chữa – bảo hành')
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
